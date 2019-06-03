from faker import Faker
from db.customer import Customer
from db.booking import Booking
from db.listings import Listings
from db.calendar import Calendar
import mongoengine
import datetime
import random
import argparse


def mongo_db_seed(db_name):
    """
    This is a sample mongodb test for populating sample data into mongodb
    :return: the db connection
    """
    mongoengine.connect(db_name, host='localhost', port=27017)
    fake = Faker()

    for x in range(10):
        Listings(
            listing_id=random.randint(8741,34875),
            name=fake.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None),
            price=str(random.random() * 100),
        ).save()

    for listing in Listings.objects:
        Calendar (
            listing_id = listing.listing_id,
            date = "2019-09-09",
            available="t",
            price=str(random.random() * 100),
        ).save()

    for x in range(3):
        Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password='12345678',
            phone=fake.phone_number(),
            customer_since=datetime.datetime.utcnow(),
            orders=[]
        ).save()

    customer = Customer.objects.first()
    listing = Listings.objects.first()
    Booking(
        customer_name = customer.first_name + " " + customer.last_name,
        customer_id = customer.id,
        listing_id = listing.listing_id,
        listing_dates = ["2019-09-09"],
        total_price = 50,
        order_status = "completed",
        order_date = datetime.datetime.utcnow(),
    ).save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("db_seed")
    parser.add_argument("db_name", type=str, help="The name of the db that you wish to populate sample seed data.")
    args = parser.parse_args()
    mongo_db_seed(args.db_name)
