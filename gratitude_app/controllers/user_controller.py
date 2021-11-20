from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db, lm
from models.users import User
from models.gratitudes import Gratitude
from schemas.user_schema import user_schema, users_schema, user_update_schema
from schemas.gratitude_schema import gratitude_schema, gratitudes_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
from pathlib import Path
import boto3

@lm.user_loader
def load_user(user):
    return User.query.get(user)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/login/')

users = Blueprint('users', __name__)


@users.route("/")
def home():
    data = {
        "page_title": "Home"
    }
    return render_template("index.html", page_data=data)

# Sign up
@users.route('/signup/', methods=['GET', 'POST'])
def signup():
    data = {
        "page_title": "Sign Up"
    }

    if request.method == 'GET':
        return render_template("signup.html", page_data=data)
    else:
        new_user = user_schema.load(request.form)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('users.get_user', user_id=new_user.user_id))

# Log in
@users.route('/login/', methods=['GET', 'POST'])
def login():
    data = {
        "page_title": "Log In",
    }
    if request.method == 'GET':
        return render_template("login.html", page_data=data)
    else:
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('users.get_user'))
        else:
            abort(401, "Login unsuccessful. Check username and password")

# Log out
@users.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/login/")

# View all users
@users.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    data = {
        "page_title": "All Users",
        "users": users_schema.dump(users)
    }
    return render_template("user_index.html", page_data=data)

# Edit logged in user's account
@users.route('/account/', methods=['GET', 'POST'])
@login_required
def edit_user():
    if request.method == 'GET':
        data = {
            "page_title": "Edit Account",
        }
        return render_template("user_details.html", page_data=data)

    else:
        user = User.query.filter_by(user_id=current_user.user_id)
        # print(request.form)
        data = user_update_schema.dump(request.form)
        print(data)
        errors = user_update_schema.validate(data)

        if errors:
            raise ValidationError(message=errors)

        user.update(data)
        db.session.commit()
        
        return redirect(url_for('users.get_user', user_id=current_user.user_id))


# Show details of current user
@users.route('/user/', methods=['GET'])
@login_required
def get_user():
    user = User.query.get_or_404(current_user.user_id)
    gratitudes = Gratitude.query.where(Gratitude.user_id == current_user.user_id)

    s3_client=boto3.client("s3")
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    # region=current_app.config["AWS_REGION"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            "Bucket": bucket_name,
            "Key": f"user_images/{user.image_filename}"
        },
        ExpiresIn=3600*24
    )
    # image_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/user_images/{user.image_filename}"
    # https://gratitude-side-app-ccc.s3.ap-southeast-2.amazonaws.com/user_images/6.png
    data = {
        "page_title": user.name,
        "user": user_schema.dump(user),
        "gratitudes": gratitudes_schema.dump(gratitudes),
        "image": image_url
    }
    # print(data)
    return render_template("user.html", page_data=data)

# Show details of a specific user
@users.route('/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    gratitudes = Gratitude.query.where(Gratitude.user_id == user_id)
    data = {
        "page_title": user.name,
        "user": user_schema.dump(user),
        "gratitudes": gratitudes_schema.dump(gratitudes)
    }
    return render_template("user.html", page_data=data)

@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


# @users.route('/users/<int:user_id>/gratitudes', methods=['GET'])
# def get_user_gratitudes(user_id):
#     gratitudes = Gratitude.query.where(Gratitude.user_id == user_id)
#     result = gratitudes_schema.dump(gratitudes)
#     if result:
#         return jsonify(result)
#     else:
#         return jsonify({"message": "No gratitudes found for this user"})

@users.route('/users/<int:user_id>/<int:gratitude_id>', methods=['GET'])
def get_user_gratitude(user_id, gratitude_id):
    user = User.query.get_or_404(user_id)
    gratitude = Gratitude.query.get_or_404(gratitude_id)
    if user.user_id == gratitude.user_id:
        result = gratitude_schema.dump(gratitude)
        return jsonify(result)
    else:
        return jsonify({"message": "There was an issue"})



# @users.route("/users/<int:user_id>/image/", methods=["POST"])
# @login_required
# def update_image(user_id):
    
#     user = User.query.get_or_404(user_id)
#     print("Printing user:-------------------------------------------------------------------------------------------------------------------------\n", user)
#     if "image" in request.files:
#         print(request.files["image"])
#         image = request.files["image"]
        
#         if Path(image.filename).suffix == ".png" or Path(image.filename).suffix == ".jpg":
#             bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
#         else:
#             return abort(400, description="Invalid file type")
        
#         if Path(image.filename).suffix == ".png":
#             print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#             print(bucket)
#             bucket.upload_fileobj(image, f"user_images/{user.image_filename}", ExtraArgs={"ContentType": "image/png", "ACL": "public-read"})
#         # else:
#         #     bucket.upload_fileobj(image, f"{user.image_filename}.jpg")
#         user = User.query.filter_by(user_id=current_user.user_id)
#         user.update({"has_image": True})
#         db.session.commit()
#         return redirect(url_for("users.get_user", user_id=user_id))

#     return abort(400, description="No image")

