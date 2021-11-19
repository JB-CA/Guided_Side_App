from main import db

# Create model for gratitude
class Gratitude(db.Model):
        __tablename__ = "gratitudes"
        gratitude_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
        image = db.Column(db.String(500))
        text = db.Column(db.String(500))

        # def __init__(self, name, user_id, image=None, text=None):
        #     self.name = name
        #     self.user_id = user_id
        #     self.image = image
        #     self.text = text

