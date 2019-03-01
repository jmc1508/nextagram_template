from models.base_model import BaseModel
from models.user import User
from flask_login import current_user
import peewee as pw


class Relationship(BaseModel):
    #Fields - what backref to add?
    follower=pw.ForeignKeyField(User, backref='idols')
    idol=pw.ForeignKeyField(User, backref='followers')

    # @staticmethod
    def get_idols(self): #Who is the user following?

        # list_following=[
         # From User, get list of users being followed by current_user
        # result=(User.select().join(Relationship, on=Relationship.idol_id).where(Relationship.follower_id==current_user.id))
        # if result:
        #     for following in result:
        #         list_following.append(following.username)
                
        # else:
        #     list_following=[]
        
        result=Relationship.get_or_none(Relationship.follower_id==current_user.id, Relationship.idol_id==self.idol_id)
        
        return result


    def count_idols(self):


        # query=(User.select(User, pw.fn.Count(Relationship.follower_id)).join(Relationship, on=Relationship.follower_id).group_by(User)).having(User.id==self.follower_id)

        idol_count=User.select().join(Relationship, on=Relationship.follower_id).where(User.id==self.follower_id).count()

        return idol_count

    def count_fans(self):


        # query = (User.select(User, pw.fn.Count(Relationship.idol_id)).join(Relationship, on=Relationship.idol_id).group_by(User)).having(User.id==self.follower_id)

        fan_count=User.select().join(Relationship, on=Relationship.idol_id).where(User.id==self.idol_id).count()

        return fan_count