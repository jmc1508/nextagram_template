from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Follower(BaseModel):
    #Fields - what backref to add?
    follower=pw.ForeignKeyField(User)
    idol=pw.ForeignKeyField(User)