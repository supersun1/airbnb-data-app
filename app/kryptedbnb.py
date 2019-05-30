from db.calendar import Calendar
from db.booking import Booking
from db.listings import Listings
# from app.auth import login_required
from datetime import datetime, timedelta
import random

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
    checkin_date = request.form.get('checkin_date')
    desired_nights = int(request.form.get('desired_nights'))
    sort_status = request.form.get("sort_by")
    calendar_listings = Calendar.objects(date=checkin_date).all()


    for cal_list in calendar_listings:
        number_gen = random.randint(1, 101)
        if number_gen % 2:
            if cal_list.available == "t":
                cal_list_specific_listing = Calendar.objects(listing_id=cal_list.listing_id).all()
                should_add = False
                for night in range(desired_nights):
                    cur_date = datetime.strptime(checkin_date, '%Y-%m-%d')
                    cur_date += timedelta(days=night+1)
                    cur_date = datetime.strftime(cur_date, "%Y-%m-%d")

                    for specific_listing in cal_list_specific_listing:
                        if specific_listing.date == cur_date and specific_listing.available == "t":
                            should_add = True
                            break

                if should_add:
                    listing = Listings.objects(listing_id=cal_list.listing_id).get()
                    listing_tuple = (listing, cal_list.date)
                    print(listing.listing_id)
                    available_listing.append(listing_tuple)

        if len(available_listing) > 9:
            break;


    available_listing = sort_by_price(available_listing, sort_status)

    return render_template('kryptedbnb/index.html', listings=available_listing)

def get_listings():
    random_available_listing = []
    listings = Listings.objects().all()
    cur_date = datetime.now().strftime("%Y-%m-%d")

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

def sort_by_price(listings, sort_type):
    if sort_type == "high_to_low":
        sorted(listings, key=lambda listing: (listing[0]).price, reverse=True)
        print(listings[0].price)
    else:
        sorted(listings, key=lambda listing: (listing[0]).price)
        return listings


#
# def create_order(copies, isbn):
#     book = Book.objects(isbn=isbn).get()
#     customer = Customer.objects(first_name="Kennth").get()
#

