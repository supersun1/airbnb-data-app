from db.booking import Booking

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

bp = Blueprint('booking', __name__, url_prefix='/booking')
