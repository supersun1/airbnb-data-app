import functools
import datetime
import mongoengine
from db.customer import Customer
from db.booking import Booking
from db.listings import Listings

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("customer", __name__, url_prefix="/customer")


@bp.route('/<string:id>/cur_user_order')
def cur_user_info(id):
    customer = Customer.objects(id=id).first()
    order = customer.orders
    has_listing="yes"

    if len(order) == 0:
        has_listing = ""

    return render_template('kryptedbnb/bookings.html', orders=customer.orders, listing=has_listing)
