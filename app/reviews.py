from db.reviews import Reviews

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

bp = Blueprint('reviews', __name__, url_prefix='/reviews')
