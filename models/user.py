from models.base_model import BaseModel
import peewee as pw



class User(BaseModel):
    name = pw.CharField(unique=False, null=True)
    email=pw.CharField(max_length=128, unique=True)
    username=pw.CharField(max_length=128, unique=True, index=False)  #Index: search by username
    password=pw.CharField(max_length=128)

    def validate(self):
        # Duplicates

        duplicate_username=User.get_or_none(User.username==self.username)
        duplicate_email=User.get_or_none(User.email==self.email)

        # Empty field
        
        if duplicate_username:
            self.errors.append('Error: username exists')
        if duplicate_email:
            self.errors.append('Error: email exists')
        if self.username=='':
            self.errors.append('Error: username not entered')
        if self.email=='':
            self.errors.append('Error: email not entered')
        if self.password=='':
            self.errors.append('Error: password not entered')