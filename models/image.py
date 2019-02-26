from models.base_model import BaseModel
import peewee as pw
from models.user import User

# Import app
from app import app

# Hybrid property import
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    # Fields
    user=pw.ForeignKeyField(User,backref="images")
    user_image_path=pw.CharField(max_length=255, null=True)

    # Hybrid property
    @hybrid_property
    def gallery_photo_url(self):
        # Refer to config.py for definitions - not directly from .env
        return f'{app.config["S3_LOCATION"]}{self.user_image_path}'