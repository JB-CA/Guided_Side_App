from main import ma 
from models.users import User
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Email, ContainsNoneOf
from marshmallow.fields import Method, Date
from marshmallow.exceptions import ValidationError
from werkzeug.security import generate_password_hash
import string

class UserSchema(ma.SQLAlchemyAutoSchema):
    user_id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=[Length(min=2, max=50), ContainsNoneOf(string.punctuation)])
    email = auto_field(required=True, validate=Email())
    password = Method(required=True, load_only=True, deserialize="load_password")
    # birthday = Date(required=False, validate=[Length(min=10, max=10)], format='%d-%m-%Y')
    mood = auto_field(required=False, validate=[Length(min=1, max=1)])

    def load_password(self, value):
        if len(value) > 6:
            return generate_password_hash(value, method='sha256')
        raise ValidationError("Password must be at least 6 characters long")

    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        # dateformat = '%d-%m-%Y'

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserSchema(partial=True)