from main import ma 
from models.users import User
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Email

class UserSchema(ma.SQLAlchemyAutoSchema):
    user_id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=[Length(min=1, max=50)])
    email = auto_field(required=True, validate=Email)
    password = auto_field(load_only=True, required=True, validate=[Length(min=1, max=50)])
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)