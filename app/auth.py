import functools
import datetime
from db.customer import Customer

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

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = Customer.objects(id=user_id).first()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        address = request.form["address"]
        phone = request.form["phone"]
        error = None

        if not email:
            error = "E-mail is required."
        elif not password:
            error = "Password is required."
        elif not first_name:
            error = "first_name is required."
        elif not last_name:
            error = "last_name is required."
        elif not address:
            error = "address is required."
        elif (
            Customer.objects(email=email).first()
            is not None
        ):
            error = "E-mail {0} is already registered.".format(email)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            Customer(
                first_name=first_name,
                last_name=last_name,
                address=address,
                email=email,
                password=generate_password_hash(password),
                phone=phone,
                customer_since=datetime.datetime.utcnow(),
                orders=[]
            ).save()

            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = Customer.objects(email=email).first()

        if user is None:
            error = "Incorrect Email."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = str(user["id"])
            return redirect(url_for("bookstore.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("bookstore.index"))
