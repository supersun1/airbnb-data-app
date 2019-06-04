from flask import redirect, url_for, g, session
from flask_dance.contrib.github import make_github_blueprint, github
from db.customer import Customer
import datetime


bp = make_github_blueprint(
    client_id="client_id",
    client_secret="client_secret",
    redirect_url='http://localhost:5000/login'
)


@bp.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    email = resp.json()["email"]
    user = Customer.objects(email=email).first()
    if user is None:
        cus = Customer(
            first_name="John",
            last_name="Doe",
            email=email,
            password="123456789",
            customer_since=datetime.datetime.utcnow(),
            phone = "",
            orders=[]
        ).save()
        session.clear()
        session["user_id"] = str(cus["id"])
        return redirect(url_for("kryptedbnb.index"))
    else:
        session.clear()
        session["user_id"] = str(user["id"])
        return redirect(url_for("kryptedbnb.index"))
