from db.calendar import Calendar
from db.booking import Booking
from db.listings import Listing
# from app.auth import login_required
import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, g
)

bp = Blueprint('kryptedbnb', __name__)

shopping_cart = []


@bp.route('/')
def index():
    available_listing = get_listings()

    return render_template('kryptedbnb/index.html', listings=available_listing)


# @bp.route('/addcart', methods=['POST'])
# # @login_required
# def add_to_cart():
#     copies = request.form.get('copies')
#     # create_order(copies, isbn)
#
#     return render_template('bookstore/order.html')
#
#
# @bp.route('/checkoutoption', methods=['POST'])
# def at_checkout():
#     if request.form['submit_btn'] == 'Keep Browsing':
#         return redirect(url_for('bookstore.index'))
#     elif request.form['submit_btn'] == 'Checkout':
#         return redirect(url_for('order.create'))


def get_listings():
    random_available_listing = []
    listings = Listing.objects.all()
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")

    for cur_list in listings:
        # available_listings = Calendar.objects(listing_id=cur_list.id).get()
        # print(available_listings.available)
        # for avail_list in available_listings:
        #     if avail_list.available is True and avail_list.date > cur_date:
        # # if available_listings.available is True and avail_list.date > cur_date:
        #         random_available_listing.append(avail_list)
        random_available_listing.append(listings)
    return random_available_listing

#
# def create_order(copies, isbn):
#     book = Book.objects(isbn=isbn).get()
#     customer = Customer.objects(first_name="Kennth").get()
#

