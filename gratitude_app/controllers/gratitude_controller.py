from flask import Blueprint, jsonify, request
from main import db
from models.gratitudes import Gratitude

gratitudes = Blueprint('gratitudes', __name__)

@gratitudes.route('/gratitudes/', methods=['GET'])
def get_gratitudes():
    gratitudes = Gratitude.query.all()
    return jsonify([gratitude.serialize for gratitude in gratitudes])

@gratitudes.route('/gratitudes/<int:gratitude_id>', methods=['GET'])
def get_gratitude(gratitude_id):
    gratitude = Gratitude.query.get_or_404(gratitude_id)
    return jsonify(gratitude.serialize)

@gratitudes.route('/gratitudes/', methods=['POST'])
def create_gratitude():
    data = request.get_json()
    name = data['name']
    user_id = data['user_id']
    image = data['image'] or None
    text = data['text'] or None
    new_gratitude = Gratitude(name, user_id, image, text)
    db.session.add(new_gratitude)
    db.session.commit()
    return jsonify(new_gratitude.serialize)

@gratitudes.route('/gratitudes/<int:gratitude_id>', methods=['PUT', 'PATCH'])
def update_gratitude(gratitude_id):
    gratitude = Gratitude.query.get(gratitude_id)
    data = request.get_json()
    gratitude.name = data['name']
    gratitude.image = data['image'] or None
    gratitude.text = data['text'] or None
    db.session.commit()
    return jsonify(gratitude.serialize)

@gratitudes.route('/gratitudes/<int:gratitude_id>', methods=['DELETE'])
def delete_gratitude(gratitude_id):
    gratitude = Gratitude.query.get(gratitude_id)
    db.session.delete(gratitude)
    db.session.commit()
    return jsonify(gratitude.serialize)