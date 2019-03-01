from models.base_model import BaseModel
from models.user import User
from flask_login import current_user
import peewee as pw


class Relationship(BaseModel):
    #Fields - what backref to add?
    follower=pw.ForeignKeyField(User, backref='idols')
    idol=pw.ForeignKeyField(User, backref='followers')

    def validate(self):
    
   
        pass

    def get_idols(self): #Who is the user following?

        list_following=[]
         # From User, get list of users being followed by current_user
        result=User.select().join(Relationship, on=Relationship.idol_id).where(Relationship.follower_id==self.follower_id)
        
        for following in result:
            list_following.append(following.username)
        
        return list_following


    def count_idols(self):

        pass

