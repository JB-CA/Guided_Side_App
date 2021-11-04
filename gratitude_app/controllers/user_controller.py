from flask import Blueprint, jsonify, request
from main import db
from models.users import User
from models.gratitudes import Gratitude

users = Blueprint('users', __name__)

@users.route("/")
def hello_world():
    return "Hello World!\n"

@users.route('/signup/')
def get_signup():
    return "This will be a sign up form\n"



@users.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize for user in users])


@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize)

@users.route('/signup/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    new_user = User(name, email, password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)

@users.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    print(data)
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify(user.serialize)

@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize)


@users.route('/users/<int:user_id>/gratitudes', methods=['GET'])
def get_user_gratitudes(user_id):
    gratitudes = Gratitude.query.where(Gratitude.user_id == user_id)
    result = [gratitude.serialize for gratitude in gratitudes]
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No gratitudes found for this user"})
