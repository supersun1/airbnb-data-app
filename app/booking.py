from db.booking import Booking
from db.calendar import Calendar
from db.customer import Customer
from datetime import datetime, timedelta
from app.auth import login_required


from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, g
)

bp = Blueprint('booking', __name__, url_prefix='/booking')

@bp.route('/')
def index():
    booking = Booking.objects
    return booking.to_json()

@bp.route('/books', methods=['GET','POST'])
@login_required
def books():

    booked_nights = []
    listing_id = int(request.form.get('listing_id'))
    print("listing id: " + str(listing_id))
    nights = int(request.form.get('nights'))
    start_date = request.form.get('date')
    cal_list = Calendar.objects(listing_id=listing_id).all()
    customer = Customer.objects(id=g.user['id']).get()
    tot_price = 0

    night_tracker = nights

    d1 = datetime.strptime(start_date, "%Y-%m-%d")


    for listing in cal_list:
        d2 = datetime.strptime(listing.date, "%Y-%m-%d")
        if listing.date >= start_date and night_tracker > 0 and abs((d2-d1).days) < night_tracker:
            booked_nights.append(listing.date)
            listing.update(available="f")
            night_tracker -= 1
            tot_price += float(listing.price[1:])
        elif night_tracker == 0:
            break

    booking = Booking(
        customer_name=customer.first_name + " " + customer.last_name,
        customer_id=customer.id,
        listing_id=str(listing_id),
        listing_dates=booked_nights,
        total_price=tot_price,
        order_status="approved",
        order_date=datetime.now(),
    ).save()

    customer.update(add_to_set__orders=booking)

    print(g.user['id'])
    return render_template("kryptedbnb/booked.html", night_count=nights)
