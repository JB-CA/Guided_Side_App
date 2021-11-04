from main import ma 
from models.users import User
from marshmallow_sqlalchemy import auto_field

class UserSchema(ma.SQLAlchemyAutoSchema):
    user_id = auto_field(dump_only=True)
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(exclude=['password'], many=True)