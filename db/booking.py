from mongoengine import*
import datetime

class Booking(Document):
    customer_name = StringField(required=True, max_length=200)

    total_price = FloatField(min_value=0)
    order_status = StringField(required=True, max_length=50, default="processing")
    order_date = DateTimeField(default=datetime.datetime.now)

