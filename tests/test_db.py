import pytest
import datetime

from db.book import Book
from db.customer import Customer
from db.inventory import Inventory
from db.order import Order
from mongoengine.errors import ValidationError


def test_entry_counts(app):
    book_count = Book.objects.count()
    assert book_count == 10
    inventory_count = Inventory.objects.count()
    assert inventory_count == 10
    customer_count = Customer.objects.count()
    assert customer_count == 10
    order_count = Order.objects.count()
    assert order_count >= 10


def test_valid_data_entry(app):
    book_input = Book(
        title="Test book title",
        isbn="Test12345",
        author="Test author",
        price="123",
        published=datetime.datetime.utcnow(),
        publisher="Test company"
    )
    book_input.save()

    # verify book is successfully saved and able to be retrieved and their values match
    book_saved = Book.objects(title=book_input.title).first()
    assert book_saved.title == book_input.title
    assert book_saved.isbn == book_input.isbn
    assert book_saved.author == book_input.author
    assert book_saved.price == book_input.price
    assert book_saved.published.strftime("%m/%d/%Y, %H:%M:%S") == book_input.published.strftime("%m/%d/%Y, %H:%M:%S")
    assert book_saved.publisher == book_input.publisher

    # verify book can be retrieved by isbn
    book_saved = Book.objects(isbn=book_input.isbn).first()
    assert book_saved.title == book_input.title
    assert book_saved.isbn == book_input.isbn
    assert book_saved.author == book_input.author
    assert book_saved.price == book_input.price
    assert book_saved.published.strftime("%m/%d/%Y, %H:%M:%S") == book_input.published.strftime("%m/%d/%Y, %H:%M:%S")
    assert book_saved.publisher == book_input.publisher

    # verify the book can be ordered by a customer
    sample_customer = Customer.objects.first()

    order = Order(
        customer_name="{} {}".format(sample_customer.first_name, sample_customer.last_name),
        books=[book_saved.id],
        shipping_address=sample_customer.address,
        total_price=book_saved.price,
        order_status="processing",
        order_date=datetime.datetime.utcnow()
    ).save()
    sample_customer.orders.append(order.id)
    sample_customer.save()

    # Look for customer by order. Customer ID should match
    order_customer = Customer.objects(orders=order.id).first()
    assert order_customer.id == sample_customer.id


def test_invalid_data_entry(app):
    invalid_book = Book(
        price="123",
        published=datetime.datetime.utcnow(),
        publisher="Test company"
    )
    with pytest.raises(ValidationError):
        invalid_book.save()
    invalid_customer = Customer (
        phone="123",
        customer_since=datetime.datetime.utcnow(),
        orders=[]
    )
    with pytest.raises(ValidationError):
        invalid_customer.save()
