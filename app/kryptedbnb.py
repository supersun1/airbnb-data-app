from kryptedbnb.calendar import Calendar
from kryptedbnb.booking import Booking
from kryptebnb.listings import Listings
# from app.auth import login_required
from datetime import datetime, timedelta
import time
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
    desired_nights = request.form.get('desired_nights')
    if desired_nights is "":
        desired_nights = 1
    else:
        desired_nights = int(desired_nights)
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
                    listing_tuple = (listing, cal_list.date, desired_nights)
                    available_listing.append(listing_tuple)

        if len(available_listing) > 9:
            break;


    available_listing = sort_by_price(available_listing, sort_status)


    return render_template('kryptedbnb/index.html', listings=available_listing)

@bp.route('/books', methods=['POST'])
def books():
    print("booking")
#     available_listing = []
#     listing_id = request.form.get('listing_id')
#     nights = request.form.get('nights')
#
#     print("booked listing: " + listing_id + " for " + nights + " nights")
#
#
#
#     return render_template('kryptedbnb/index.html', listings=available_listing)




@bp.route('/moreInfo', methods=['GET', 'POST'])
def more_info():
    dates = []
    available_listing = []
    room_id = request.form.get('listing_id')
    room_id = int(room_id)
    listing = Listings.objects(listing_id=room_id).get()

    print(listing)
    available_dates = Calendar.objects(listing_id=room_id).all()

    for date in available_dates:
        if date.available == "t":
            dates.append(date.date)
        if len(available_dates) > 2:
            break

    # dates.append("2019-08-08")

    listing_tuple = (listing, dates, "exist")
    print(listing['name'])
    available_listing.append(listing_tuple)
    return render_template('kryptedbnb/moreinfo.html', listing=listing_tuple)







def get_listings():
    random_available_listing = []
    seen = []
    random.seed(int(time.time()))
    listings = Listings.objects().all()
    cur_date = datetime.now().strftime("%Y-%m-%d")
    calendar_listings = Calendar.objects(available="t").all()

    for cal_list in calendar_listings:
        number_gen = random.randint(1, 101)
        if number_gen % 2:
            if cal_list.listing_id in seen:
                continue
            seen.append(cal_list.listing_id)

            if cal_list.date > cur_date:
                listing = Listings.objects(listing_id=cal_list.listing_id).get()
                listing_tuple = (listing, cal_list.date, 1)
                random_available_listing.append(listing_tuple)

            if len(random_available_listing) > 9:
                break

    return random_available_listing

def sort_by_price(listings, sort_type):
    if sort_type == "high_to_low":
        sorted(listings, key=lambda listing: (listing[0]).price, reverse=True)
        print(listings[0].price)
    else:
        sorted(listings, key=lambda listing: (listing[0]).price)
        return listings
