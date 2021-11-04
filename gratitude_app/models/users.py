from main import db

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
