
from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #JUST ADDED

# Import app
from app import app

# Hybrid property import
from playhouse.hybrid import hybrid_property



class User(BaseModel,UserMixin): #UserMixin - package that adds in Flask-Login User attributes
    name = pw.CharField(unique=False, null=True)
    email=pw.CharField(max_length=128, unique=True)
    username=pw.CharField(max_length=128, unique=True, index=False)  #Index: search by username
    password=pw.CharField(max_length=128)
    profile_photo_path=pw.CharField(max_length=255,null=True, default="placeholder_profile_photo.jpg")
    private=pw.BooleanField(default=True)


    def validate(self):
        # Error Validation

        duplicate_username=User.get_or_none(User.username==self.username)
        duplicate_email=User.get_or_none(User.email==self.email)
        


        if len(self.password)==93:
            pass
            # We know that password has not been changed as it is length of hashed passwrod
        else:

            if len(self.password)<8 or len(self.password)>15:
                self.errors.append('Error: password must be 8 & 15')
            else:
                self.password=generate_password_hash(self.password)

        # Empty field
        if duplicate_username and duplicate_username.username != User.get_by_id(self.id).username:
            self.errors.append('Error: username exists')
        if duplicate_email and duplicate_email.email != User.get_by_id(self.id).email:
            self.errors.append('Error: email exists')
        if self.username=='':
            self.errors.append('Error: username not entered')
        if self.email=='':
            self.errors.append('Error: email not entered')
        if self.password=='':
            self.errors.append('Error: password not entered')

        #Login validation
        
        if self.username=='':
            self.errors.append('Error: username not entered')
        if self.password=='':
            self.errors.append('Error: password not entered')

    # Hybrid property
    @hybrid_property
    def profile_photo_url(self):
        # Refer to config.py for definitions - not directly from .env
        return f'{app.config["S3_LOCATION"]}{self.profile_photo_path}'

