from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from os import environ

db_user, db_pass, db_name, db_domain = (
    environ.get(item) for item in ["DB_USER", "DB_PASS", "DB_NAME", "DB_DOMAIN"]
)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Gratitude(db.Model):
    __tablename__ = "gratitudes"
    gratitude_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image = db.Column(db.String(500))
    text = db.Column(db.String(500))

    def __init__(self, name, user_id, image=None, text=None):
        self.name = name
        self.user_id = user_id
        self.image = image
        self.text = text

    @property
    def serialize(self):
        return {
            'gratitude_id': self.gratitude_id,
            'user_id': self.user_id,
            'name': self.name,
            'image': self.image,
            'text': self.text
        }

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    gratitudes = db.relationship("Gratitude", backref="users")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @property
    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }

# db.drop_all()
db.create_all()


@app.route("/")
def hello_world():
    return "Hello World!\n"

@app.route('/signup/')
def get_signup():
    return "This will be a sign up form\n"

@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize for user in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize)

@app.route('/signup/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    new_user = User(name, email, password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)

@app.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    print(data)
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify(user.serialize)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize)

@app.route('/gratitudes/', methods=['GET'])
def get_gratitudes():
    gratitudes = Gratitude.query.all()
    return jsonify([gratitude.serialize for gratitude in gratitudes])

@app.route('/gratitudes/<int:gratitude_id>', methods=['GET'])
def get_gratitude(gratitude_id):
    gratitude = Gratitude.query.get_or_404(gratitude_id)
    return jsonify(gratitude.serialize)


@app.route('/users/<int:user_id>/gratitudes', methods=['GET'])
def get_user_gratitudes(user_id):
    gratitudes = Gratitude.query.where(Gratitude.user_id == user_id)
    result = [gratitude.serialize for gratitude in gratitudes]
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No gratitudes found for this user"})


@app.route('/gratitudes/', methods=['POST'])
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

@app.route('/gratitudes/<int:gratitude_id>', methods=['PUT', 'PATCH'])
def update_gratitude(gratitude_id):
    gratitude = Gratitude.query.get(gratitude_id)
    data = request.get_json()
    gratitude.name = data['name']
    gratitude.image = data['image'] or None
    gratitude.text = data['text'] or None
    db.session.commit()
    return jsonify(gratitude.serialize)

@app.route('/gratitudes/<int:gratitude_id>', methods=['DELETE'])
def delete_gratitude(gratitude_id):
    gratitude = Gratitude.query.get(gratitude_id)
    db.session.delete(gratitude)
    db.session.commit()
    return jsonify(gratitude.serialize)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)