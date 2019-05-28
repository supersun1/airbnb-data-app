from mongoengine import*

class Calendar(Document):
    listing_id = StringField(required=True, max_length=200)
    date = DateTimeField()
    available = BooleanField(required=True, default=False)
    price = FloatField(min_value=0)
