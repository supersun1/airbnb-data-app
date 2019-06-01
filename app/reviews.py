from db.reviews import Reviews
from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

bp = Blueprint('reviews', __name__, url_prefix='/reviews')



@bp.route('/addreviews')
def add_review():
    listing_id = request.form.get('listing_id')
    review_input = request.form.get('review_input')
    customer_id = request.form.get('customer_id')

    review = Reviews(
        listing_id=listing_id,
        date = datetime.now(),
        reviewer_id = customer_id,
        reviewer_name = "Gangsta G",
        comments = review_input
    ).save()