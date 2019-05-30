from db.listings import Listings

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

bp = Blueprint('listings', __name__, url_prefix='/listings')
