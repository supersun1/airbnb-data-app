from mongoengine import*

class Calendar(Document):
    listing_id = StringField(required=True, max_length=200)
    date = StringField(required=True)
    available = StringField(required=True)
    price = StringField(min_value=0)
