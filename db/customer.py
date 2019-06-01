from mongoengine import*
import datetime
from db.booking import Booking

class Customer(Document):
    first_name = StringField(required=True, max_length=200)
    last_name = StringField(required=True, max_length=200)
    email = StringField(required=True, max_length=50, unique=True, regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    password = StringField(required=True, min_length=8)
    phone = StringField(default=datetime.datetime.now)
    customer_since = DateTimeField(default=datetime.datetime.utcnow())
    orders = ListField(ReferenceField(Booking))

