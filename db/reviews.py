from mongoengine import*

class Reviews(Document):
    listing_id = StringField(required=True, max_length=200)
    id = StringField(required=True, max_length=200)
    date = DateTimeField()
    reviewer_id = StringField(required=True, max_length=200)
    reviewer_name = StringField(required=True, max_length=200)
    comments = StringField(required=True, max_length=20000)
