from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    # email=pw.TextField(unique=True)
    # username=pw.TextField(unique=True)
    # pass