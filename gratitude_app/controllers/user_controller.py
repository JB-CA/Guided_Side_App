from flask import Blueprint, jsonify, request, render_template
from main import db
from models.users import User
from models.gratitudes import Gratitude
from schemas.user_schema import user_schema, users_schema
from schemas.gratitude_schema import gratitudes_schema

users = Blueprint('users', __name__)

@users.route("/")
def hello_world():
    data = {
        "page_title": "Hello World",
    }
    return render_template("base.html", page_data=data)
    # return "Hello World!\n"

@users.route('/signup/')
def get_signup():
    return "This will be a sign up form\n"

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
    return jsonify(user_schema.dump(user))

@users.route('/signup/', methods=['POST'])
def create_user():

    new_user = user_schema.load(request.get_json())
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user)), 201

@users.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = user_schema.dump(request.get_json())
    if data:
        user.update(data)
    # print(data)
    # user.name = data['name']
    # user.email = data['email']
    # user.password = data['password']
        db.session.commit()
    return jsonify(user_schema.dump(user))

@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))


@users.route('/users/<int:user_id>/gratitudes', methods=['GET'])
def get_user_gratitudes(user_id):
    gratitudes = Gratitude.query.where(Gratitude.user_id == user_id)
    result = gratitudes_schema.dump(gratitudes)
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No gratitudes found for this user"})
