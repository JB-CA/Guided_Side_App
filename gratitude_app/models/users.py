from main import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mood = db.Column(db.String(1), nullable=False, server_default="😀")
    # birthday = db.Column(db.Date, nullable=True, default="01-01-2001")

    gratitudes = db.relationship("Gratitude", backref="users", cascade="all, delete-orphan")

    def get_id(self):
        return self.user_id

    @property
    def first_name(self):
        return self.name.split(" ")[0]


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.name}>"