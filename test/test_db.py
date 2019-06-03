import pytest
import datetime

from db.calendar import Calendar
from db.booking import Booking
from db.reviews import Reviews
from db.listings import Listings
from db.customer import Customer

def test_entry_counts(app):
    book_count = Booking.objects.count()
    assert book_count == 1
    calendar_count = Calendar.objects.count()
    assert calendar_count >= 10
    customer_count = Customer.objects.count()
    assert customer_count == 3
    listing_count = Listings.objects.count()
    assert listing_count >= 10


