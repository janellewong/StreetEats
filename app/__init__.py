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
import json

load_dotenv()

app = Flask(__name__)


lat, long = api_location()
ENDPOINT_YELP, HEADERS_YELP = apiYelp()

# app.config[ "SQLALCHEMY_DATABASE_URI" ] = "postgresql://postgres:pass@localhost:5432/streeteatsdb"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def getListNames(userId):
    listName = []
    from .db import Lists, db

    # get list names from user_id_fk
    listIds = db.session.query(Lists).filter_by(user_id_fk=1).all()
    for listId in listIds:
        print(listId.list_name, flush=True)
        listName.append(listId.list_name)

    return listName


## todo return friends
def getFriends(userId):
    from .db import friends, db

    # get names from friends table from user_id_fk
    userIds = db.session.query(friends).filter_by(user_id_fk=1).all()
    for userId in userIds:
        print(userId.friend_id, flush=True)


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


idList = []  # for global array declaration


@app.route("/like-business", methods=["POST"])
def likeBusiness():
    business_id = request.form.get("business-id")
    global idList
    idList = ["aarBX0VyJbjMACGCcMrfEQ", "U8tIgXZ0T--8ZNEVoDap0g"]  # TESTING PURPOSE
    # DB DATA HAS BEEN COMMENTED OUT FOR TESTING PURPOSES
    """ from .db import BusinessList, listscontents, db

    business_data = request.form.get("business-id").split(", ")
    business_id = business_data[0].replace("'", "").replace(")", "").replace("(", "")
    business_name = business_data[1].replace("'", "").replace(")", "").replace("(", "")
    # print(business_id, flush=True)
    # print(business_name, flush=True)

    # insert into business table
    add_business = BusinessList(business_id=business_id, business_name=business_name)
    db.session.add(add_business)
    db.session.commit()

    # insert into listscontents table
    statement = listscontents.insert().values(list_id_fk=1, business_id_fk=business_id)
    db.session.execute(statement)
    db.session.commit()

    # Read from listscontents table
    global idList
    ids = db.session.query(listscontents).filter_by(list_id_fk=1).all()
    for id in ids:
        print(id.business_id_fk)
        idList.append(id.business_id_fk) """
    #### returns business ids from a list == 1 #####
    # 4qyjRhjEgWGHPjgYWkBy8g
    # rCevbj5Zovz1sNqaEMlSNA
    # 1TCm5Z71hpPaAl0PXr6S6g
    # glhCxpZ4OdUkXPp0jIqvPg
    # pzg5nXrMocCzQIoTf57QJw

    # ids = db.session.query(listscontents).filter_by(list_id_fk=1).all()
    # print(ids)
    #### returns an array of (list_id_fk, 'business_id_fk'), will need to extract ###
    # [(1, '4qyjRhjEgWGHPjgYWkBy8g'), (1, 'rCevbj5Zovz1sNqaEMlSNA'), (1, '1TCm5Z71hpPaAl0PXr6S6g')]

    return '{"id":"%s","success":true}' % business_id

    # return idList


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
    # listName = getListNames(1)
    listName = ["Food", "Coffee", "Good Stuff!!"]  # TESTING PURPOSES
    return render_template(
        "userpage.html", title="My Account", url=os.getenv("URL"), names=listName
    )


@app.route("/list/<listName>", methods=["POST", "GET"])
def listpage(listName):
    idList1 = ["aarBX0VyJbjMACGCcMrfEQ", "U8tIgXZ0T--8ZNEVoDap0g"]  # TESTING PURPOSES
    # THIS WORKS NOW
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "restaurantLiked.json")
    with open(json_url, "w") as file1:
        stuff = {"liked_businesses": []}
        json.dump(stuff, file1)
    file1.close()

    for id in idList1:
        ENDPOINT_YELPB = yelpBusinessInfo(id)
        responseB = requests.get(url=ENDPOINT_YELPB, headers=HEADERS_YELP)
        businessData = responseB.json()
        print(businessData)

        # extract data from businessData to append to restaurantLiked.json
        id1 = businessData["id"]
        name = businessData["name"]
        price = businessData["price"]
        rating = businessData["rating"]
        phone = businessData["display_phone"]
        address = businessData["location"]["address1"]

        new_data = {
            "id": id1,
            "name": name,
            "price": price,
            "rating": rating,
            "phone": phone,
            "address": address,
        }

        # idea: first clear the json file THEN follow through with code to append so there is no overlap in data

        # this opens the json file and appends data to it to get it to display in html
        with open(json_url, "r+") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)

            # Join new_data with file_data inside emp_details
            file_data["liked_businesses"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)

        data = json.load(open(json_url))
        print(data)

    return render_template(
        "listpage.html", title="My List", url=os.getenv("URL"), data=data
    )


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
