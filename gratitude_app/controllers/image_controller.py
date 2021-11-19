from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.users import User
import boto3

user_images = Blueprint('user_images', __name__)

@user_images.route("/users/<int:user_id>/image/", methods=["POST"])
def update_image(user_id):
    
    user = User.query.get_or_404(user_id)
    
    if "image" in request.files:
        
        image = request.files["image"]
        
        if Path(image.filename).suffix != ".png":
            return abort(400, description="Invalid file type")
        
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, user.image_filename)


        return redirect(url_for("users.get_user", user_id=user_id))

    return abort(400, description="No image")
