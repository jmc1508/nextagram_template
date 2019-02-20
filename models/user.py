from models.base_model import BaseModel
import peewee as pw



class User(BaseModel):
    name = pw.CharField(unique=False)
    email=pw.CharField(max_length=128, unique=True)
    username=pw.CharField(max_length=128, unique=True, index=False)  #Index: search by username
    password=pw.CharField(max_length=128)
