from db.calendar import Calendar
from db.booking import Booking
from db.listings import Listings
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


# @bp.route('/checkoutoption', methods=['POST'])
# def at_checkout():
#     if request.form['submit_btn'] == 'Keep Browsing':
#         return redirect(url_for('bookstore.index'))
#     elif request.form['submit_btn'] == 'Checkout':
#         return redirect(url_for('order.create'))

@bp.route('/search', methods=['POST'])
def search():
    available_listing = []
    desired_date = request.form.get('desired_date')
    calendar_listings = Calendar.objects(date=desired_date).all()
    print("here")
    print(calendar_listings)
    # for listing in calendar_listings:
    #     if listing.available:
    #         available_listing.append(listing)

    return render_template('kryptedbnb/index.html', listings=available_listing)

def get_listings():
    random_available_listing = []
    listings = Listings.objects().all()
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")

    for listing in listings:
        calendar_listings = Calendar.objects(listing_id=listing.listing_id).all()
        for cal_list in calendar_listings:
            if cal_list.date > cur_date:
                listing_tuple = (listing, cal_list.date)
                random_available_listing.append(listing_tuple)

                break;
        if len(random_available_listing) > 10:
            break;
    return random_available_listing

#
# def create_order(copies, isbn):
#     book = Book.objects(isbn=isbn).get()
#     customer = Customer.objects(first_name="Kennth").get()
#

