import os
from flask import Flask, render_template, request, g
from dotenv import load_dotenv
import requests
from flask import request
from . import api
from app.api import api_location
from app.api import apiYelp
from app.api import yelpReviews
from app.api import yelpBusinessInfo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)


lat, long = api_location()
ENDPOINT_YELP, HEADERS_YELP = apiYelp()

#app.config[ "SQLALCHEMY_DATABASE_URI" ] = "postgresql://postgres:pass@localhost:5432/streeteatsdb"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
	user=os.getenv('POSTGRES_USER'),
	passwd=os.getenv('POSTGRES_PASSWORD'),
	host=os.getenv('POSTGRES_HOST'),
	port=5432,
	table=os.getenv('POSTGRES_DB'))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class user_category:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def repr(self):
        return self.type


# restaurants
@app.route("/", methods=["GET", "POST"])
def index():
    testLocation = "toronto"
    category = ""
    city = None

    if request.method == "POST":
        city = request.form.get("city")
        selection = request.form.get("type")
        S = user_category(selection, testLocation)
        category = S.repr()

    if city:
        PARAMETERS_YELP = {
            "term": category,
            "limit": 50,
            "offset": 50,
            "radius": 10000,
            "location": city,
        }
    else:
        PARAMETERS_YELP = {
            "term": category,
            "limit": 50,
            "offset": 50,
            "radius": 10000,
            "latitude": lat,
            "longitude": long,
        }

    # check if it is already in the database
    # if it is in , return it from db
    # if not, add to database and return to user

    response = requests.get(
        url=ENDPOINT_YELP, params=PARAMETERS_YELP, headers=HEADERS_YELP
    )
    business_data = response.json()

    # choose list
    # is business id already in db-list?
    # if it is, do nothing
    # if not, add to database

    # print(business_data)

    # if logged in, do this (figure out user session)
    return render_template(
        "index.html",
        title="StreetEats",
        url=os.getenv("URL"),
        data=business_data,
    )

    # if not logged in, do this
    # return render_template("userhomepage.html", title="StreetEats", url=os.getenv("URL"), data=business_data,)


@app.route("/like-business", methods=["POST"])
def likeBusiness():
    business_id = request.form.get("business-id")

    # Save to db or something

    return '{"id":"%s","success":true}' % business_id


@app.route("/restaurant/<name>", methods=["POST"])
def restaurant(name):

    id = request.form.get("id")
    ENDPOINT_YELPR = yelpReviews(id)
    ENDPOINT_YELPB = yelpBusinessInfo(id)

    # reviews
    responseR = requests.get(url=ENDPOINT_YELPR, headers=HEADERS_YELP)
    review_data = responseR.json()

    # business info
    responseB = requests.get(url=ENDPOINT_YELPB, headers=HEADERS_YELP)
    b_data = responseB.json()
    return render_template(
        "restodetails.html", name=name, reviews=review_data, businessData=b_data
    )


# create health end point
@app.route("/health")
def check():
    return "Working"


@app.route("/userhomepage")
def userhomepage():
    return render_template("userhomepage.html", title="Homepage", url=os.getenv("URL"))


@app.route("/userpage")
def userpage():
    return render_template("userpage.html", title="My Account", url=os.getenv("URL"))


@app.route("/listpage")
def listpage():
    return render_template("listpage.html", title="My List", url=os.getenv("URL"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        from .db import UserModel, db

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            # table = ("INSERT INTO lists( question) VALUES(%s,%s)", (1003, str(request_data['question'])))
            # db.execute_query(table)
            # app.logger.info("adding questions")
            print(new_user.id)
            # Return login page upon successful registration
            return render_template("login.html")
        else:
            return error, 418

    # Return a register page
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    from .db import UserModel

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            # Return home page upon successful registration, assuming it's "index.html"
            return index()
        else:
            return error, 418

    # Return a login page
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
