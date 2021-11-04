from main import ma 
from models.gratitudes import Gratitude
from marshmallow_sqlalchemy import auto_field

class GratitudeSchema(ma.SQLAlchemyAutoSchema):
    gratitude_id = auto_field(dump_only=True)
    class Meta:
        model = Gratitude
        include_fk = True
        load_instance = True

gratitude_schema = GratitudeSchema()
gratitudes_schema = GratitudeSchema(many=True)