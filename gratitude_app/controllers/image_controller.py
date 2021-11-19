from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.users import User
import boto3

user_images = Blueprint('user_images', __name__)

@user_images.route("/users/<int:user_id>/image/", methods=["POST"])
def update_image(user_id):
    
    user = User.query.get_or_404(user_id)
    print("Printing user:-------------------------------------------------------------------------------------------------------------------------\n", user)
    if "image" in request.files:
        print(request.files["image"])
        image = request.files["image"]
        
        if Path(image.filename).suffix == ".png" or Path(image.filename).suffix == ".jpg":
            bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        else:
            return abort(400, description="Invalid file type")
        
        if Path(image.filename).suffix == ".png":
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print(bucket)
            bucket.upload_fileobj(image, f"user_images/{user.image_filename}", ExtraArgs={"ContentType": "image/png", "ACL": "public-read"})
        # else:
        #     bucket.upload_fileobj(image, f"{user.image_filename}.jpg")

        return redirect(url_for("users.get_user", user_id=user_id))

    return abort(400, description="No image")

