from models.base_model import BaseModel
import peewee as pw



class User(BaseModel):
    name = pw.CharField(unique=False, null=True)
    email=pw.CharField(max_length=128, unique=True)
    username=pw.CharField(max_length=128, unique=True, index=False)  #Index: search by username
    password=pw.CharField(max_length=128)

    def validate(self):
        duplicate_username=User.get_or_none(User.username==self.username)
        

        if duplicate_username:
            self.errors.append('Error: your username is not unique')