from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, session
from main import db, lm
from models.users import User
from models.gratitudes import Gratitude
from schemas.user_schema import user_schema, users_schema, user_update_schema
from schemas.gratitude_schema import gratitude_schema, gratitudes_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

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
def get_signup():
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
            return redirect(url_for('users.get_user', user_id=user.user_id))
        else:
            abort(401, "Login unsuccessful. Check username and password")

# Log out
@users.route('/logout/', methods=['GET', 'POST'])
# @login_required
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
        data = user_update_schema.dump(request.form)
        errors = user_update_schema.validate(data)

        if errors:
            raise ValidationError(message=errors)

        user.update(data)
        db.session.commit()
        
        return redirect(url_for('users.get_user', user_id=current_user.user_id))


# Show details of a single user
@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
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

