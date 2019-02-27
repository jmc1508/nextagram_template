from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

# Import app
from app import app

# Hybrid property import
from playhouse.hybrid import hybrid_property


class Donation(BaseModel):
    # Fields
    image=pw.ForeignKeyField(Image,backref="donations") #image id
    amount = pw.DecimalField(decimal_places=2) #payment amount
    donor=pw.ForeignKeyField(User, backref="donor") #donor id
    currency=pw.CharField(default="USD")
    transaction_id=pw.CharField(unique=True) #Transaction id that is returned

    # def validate(self):

    #     # Amount
    #     if float(self.amount)>float(2000):
    #         self.errors.append('Error: You cannot donate more than 2,000')

        
        