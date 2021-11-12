from flask import Blueprint, jsonify, request, render_template, redirect, url_for
# from werkzeug.utils import redirect
from main import db
from models.users import User
from models.gratitudes import Gratitude
from schemas.user_schema import user_schema, users_schema
from schemas.gratitude_schema import gratitude_schema, gratitudes_schema

users = Blueprint('users', __name__)

@users.route("/")
def hello_world():
    data = {
        "page_title": "Home"
        # "active": "active"
    }
    return render_template("index.html", page_data=data)


@users.route('/signup/')
def get_signup():
    data = {
        "page_title": "Sign Up",
        "page_message": "This will be a sign up form\n"
    }
    return render_template("signup.html", page_data=data)

@users.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    data = {
        "page_title": "All Users",
        "users": users_schema.dump(users)
    }
    return render_template("user_index.html", page_data=data)

# @users.route('/users/', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     return jsonify(users_schema.dump(users))


@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    gratitudes = Gratitude.query.where(Gratitude.user_id == user_id)
    # result = gratitudes_schema.dump(gratitudes)
    data = {
        "page_title": user.name,
        "user": user_schema.dump(user),
        "gratitudes": gratitudes_schema.dump(gratitudes)
    }
    return render_template("user.html", page_data=data)

@users.route('/signup/', methods=['POST'])
def create_user():
    new_user = user_schema.load(request.form)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('users.get_users'))
    # return redirect('/users/')

    # return jsonify(user_schema.dump(new_user)), 201

@users.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = user_schema.dump(request.get_json())
    if data:
        user.update(data)
        db.session.commit()
    return jsonify(user_schema.dump(user))

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

