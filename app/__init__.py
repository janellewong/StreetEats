import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
from flask import request, redirect, url_for
from sqlalchemy.sql.expression import true
from app.api import api_location
from app.api import apiYelp
from app.api import yelpReviews
from app.api import yelpBusinessInfo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy.sql import select, and_
from flask import Flask, g
from flask import session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

load_dotenv()

app = Flask(__name__)


ENDPOINT_YELP, HEADERS_YELP = apiYelp()
login_manager = LoginManager()
login_manager.init_app(app)


def get_my_ip():

    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        print(request.environ["REMOTE_ADDR"], flush=True)
        ip = request.environ["REMOTE_ADDR"]
        return ip
    else:
        print(request.environ["HTTP_X_FORWARDED_FOR"], flush=True)  # if behind a proxy
        ip = request.environ["HTTP_X_FORWARDED_FOR"]

        return ip


@login_manager.user_loader
def load_user(user_id):
    # from .db import UserModel
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return UserModel.query.filter_by(user_id=int(user_id)).first()


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

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

friends = db.Table(
    "friends",
    db.Column(
        "user_id_fk",
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "friend_id",
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# create user table
class UserModel(db.Model):
    __tablename__ = "users"
    # Add user id, username, password columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    lists = db.relationship("Lists", backref="List_OwnerID")
    # User has lists that refers to Lists db
    friendship = db.relationship(
        "UserModel",
        secondary=friends,
        primaryjoin=user_id == friends.c.user_id_fk,
        secondaryjoin=user_id == friends.c.friend_id,
        backref="followed_by",
    )

    def __init__(self, username, password):
        # self.user_id = user_id
        self.username = username
        self.password = password

    def is_active(self):
        return True

    def is_active(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return int(self.user_id)

    def __repr__(self):
        return f"<User {self.username}>"


listscontents = db.Table(
    "listscontents",
    db.Column(
        "list_id_fk", db.Integer, db.ForeignKey("lists.list_id", ondelete="CASCADE")
    ),
    db.Column(
        "business_id_fk",
        db.String,
        db.ForeignKey("businesses.business_id", ondelete="CASCADE"),
    ),
)


class Lists(db.Model):
    __tablename__ = "lists"
    # Add id number of user who owns list, name of list, list_id number columns
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String())
    user_id_fk = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE")
    )
    listContents = db.relationship(
        "BusinessList",
        secondary=listscontents,
        backref=db.backref("lists", lazy="dynamic"),
        lazy="dynamic",
    )
    # List db has businesses that refers to BusinessList/businesses db

    ### Need Help with where / how to connect and assign attributes for each user here
    def __init__(self, list_name, user_id_fk):
        self.list_name = list_name
        self.user_id_fk = user_id_fk

    # def __repr__(self):
    #    return f"User {username} has list {}." # confused here
    #    self.business_id = #RETRIEVE from api
    #    self.business_name = #Restrieve id from api then retrieve name
    #    self.list_id = #Retrieve from lists db


class BusinessList(db.Model):
    __tablename__ = "businesses"
    # Add id number of list, name of business, business_id columns
    business_id = db.Column(db.String, primary_key=True)
    business_name = db.Column(db.String())
    # list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"))

    ### Need Help with where / how to connect and assign attributes for each business here
    def __init__(self, business_id, business_name):
        self.business_id = business_id
        self.business_name = business_name
        # self.list_id = list_id

    # def __repr__(self):
    #    return f"User {username} has list {}." # confused here
    #    self.business_id = #RETRIEVE from api
    #    self.business_name = #Restrieve id from api then retrieve name
    #    self.list_id = #Retrieve from lists db


load_dotenv()
db.create_all()

# add list id and business id to listscontents table
def addRestaurantToList(listId, businessId):
    # from .db import listscontents, db

    # insert into listscontents table
    statement = listscontents.insert().values(
        list_id_fk=listId, business_id_fk=businessId
    )
    db.session.execute(statement)
    db.session.commit()


# gets a list of names of list
def getListNames(userId):
    listName = []
    # from .db import Lists, db

    # get list names from user_id_fk
    listIds = db.session.query(Lists).filter_by(user_id_fk=current_user.user_id).all()
    for listId in listIds:
        print(listId.list_name, flush=True)
        listName.append(listId.list_name)

    return listName


# take listIds from Lists table db
def getListIds(userId):
    listIds = []
    # from .db import db, Lists

    stmt = select([Lists.list_id]).where(Lists.user_id_fk == userId)
    results = db.session.execute(stmt).scalars()
    for result in results:
        listIds.append(result)

    return listIds


## return business ids based on list ids from listscontents
def getBusinessId(list_id):
    idList = []

    # from .db import listscontents, db

    # Read from listscontents table
    ids = (
        db.session.query(listscontents).filter_by(list_id_fk=list_id).all()
    )  # list id parameter
    for id in ids:
        print(id.business_id_fk)
        idList.append(id.business_id_fk)

    return idList


## return friends ids
def getFriends(userId):
    # from .db import friends, db

    # get names from friends table from user_id_fk
    userIds = db.session.query(friends).filter_by(user_id_fk=1).all()
    for userId in userIds:
        print(userId.friend_id, flush=True)


# creates a default liked list for every registered user
def createLikedList(userId):
    # from .db import Lists, db
    add_liked_list = Lists(list_name="Liked", user_id_fk=userId)
    db.session.add(add_liked_list)
    print(userId, flush=True)
    db.session.commit()


def createList(userId, listName):
    # from .db import Lists, db

    add_list = Lists(list_name=listName, user_id_fk=int(userId))

    db.session.add(add_list)
    print(userId, listName, flush=True)
    db.session.commit()


class user_category:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def repr(self):
        return self.type


# restaurants
@app.route("/", methods=["GET", "POST"])
def index():
    ip = get_my_ip()
    lat, long = api_location(ip)
    print(ip, flush=True)
    testLocation = "toronto"
    category = ""
    city = None

    if current_user.is_active:
        print(f"The current user logged in: {current_user.user_id}", flush=True)
        ## add dynamic user
        listNames = getListNames(current_user.user_id)
    else:
        print("No active user", flush=True)

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
    if current_user.is_active:
        return render_template(
            "userhomepage.html",
            title="StreetEats",
            url=os.getenv("URL"),
            data=business_data,
            listName=listNames,
        )
    else:

        # if not logged in, do this
        return render_template(
            "index.html",
            title="StreetEats",
            url=os.getenv("URL"),
            data=business_data,
        )


business_id = ""


@login_required
@app.route("/like-business", methods=["POST"])
def likeBusiness():
    if current_user.is_active:
        global business_id
        # business_id = request.form.get("business-id")

        # from .db import BusinessList, db

        business_data = request.form.get("business-id").split(", ")
        business_id = (
            business_data[0].replace("'", "").replace(")", "").replace("(", "")
        )
        business_name = (
            business_data[1].replace("'", "").replace(")", "").replace("(", "")
        )
        # print(business_id, flush=True)
        # print(business_name, flush=True)

        # insert into business table
        add_business = BusinessList(
            business_id=business_id, business_name=business_name
        )
        db.session.add(add_business)
        db.session.commit()

        return '{"id":"%s","success":true}' % business_id
    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


@login_required
@app.route("/modal-like", methods=["POST"])
def modalLike():
    if current_user.is_active:
        ## add dynamic user
        listNames = getListNames(current_user.user_id)
        listIds = getListIds(current_user.user_id)
        listname = request.form.get("modal-liked")
        # print(listname)

        for entry in listNames:
            if entry == listname:
                index = listNames.index(entry)
                list_id = listIds[index]
        # print(list_id)

        # print(listIds, flush=True)

        bIds = getBusinessId(list_id)
        # print(f"Business Ids: {bIds}", flush=True)

        # do not allow duplicates
        if business_id not in bIds:
            addRestaurantToList(list_id, business_id)

        return '{"id":"%s","success":true}' % listname

    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


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


@app.route("/removeList", methods=["POST"])
def removeList():
    removeName = request.form.get("removelist")
    listNames = getListNames(current_user.user_id)
    listIds = getListIds(current_user.user_id)

    for entry in listNames:
        if entry == removeName:
            index = listNames.index(entry)
            list_id_remove = listIds[index]  # LIST ID TO REMOVE
            # print(f"list_id_remove: {list_id_remove}", flush=True)
            # return list_id_remove
            # db.session.query(listscontents).filter(listscontents.list_id_fk == list_id_remove).delete()
            # Lists.query.filter(Lists.list_id == list_id_remove).delete()
            # stmt = select([listscontents.list_id_fk]).where(listscontents.list_id_fk == list_id_remove).delete()
            # stmt = listscontents.delete().where(Users.id.in_())
            # results = select([listscontents.list_id_fk]).where(listscontents.list_id_fk == list_id_remove)
            # for result in results:
            #     db.session.delete(result)
            #     db.session.commit()
            Lists.query.filter(Lists.list_id == list_id_remove).delete()

            # results.delete()
            db.session.commit()
    return redirect(url_for("userpage"), code=302)

    # result = findId(removeName, listNames, listIds)
    # print(f"Result: {result}", flush=True)
    # # print(f"listNames: {listNames}", flush=True)

    # INSERT DB CODE TO REMOVE THE LIST ID FROM THE LISTID DB
    # return '{"id":"%s","success":true}' % list_id_remove


@app.route("/removeResto", methods=["POST"])
def removeResto():
    restoID = request.form.get("removeResto")  # pull restaurant id AND list name
    listName = request.form.get("listName_Resto")
    listNames = getListNames(current_user.user_id)
    listIds = getListIds(current_user.user_id)

    # first get the list_id of the list the restaurant is stored in
    for entry in listNames:
        if entry == listName:
            index = listNames.index(entry)
            list_id = listIds[index]  # LIST ID

    idList = getBusinessId(list_id)  # now get the business ids array of that list id

    # if restaurantid is found in the businessid array for that list delete the restaurant id
    for id in idList:
        if restoID == id:
            print("REMOVE restoID from DATABASE")  # DB CODE INSERT HERE

    return '{"id":"%s","success":true}' % restoID


@app.route("/userhomepage", methods=["POST"])
def userhomepage():

    ip = get_my_ip()
    lat, long = api_location(ip)

    if current_user.is_active:
        testLocation = "toronto"
        category = ""
        city = None

        # check if it is already in the database
        # if it is in , return it from db
        # if not, add to database and return to user

        ## add dynamic user
        listNames = getListNames(1)

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
            "userhomepage.html",
            title="Homepage",
            url=os.getenv("URL"),
            data=business_data,
            listName=listNames,
        )
    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


@login_required
@app.route("/settings")
def settings():
    if current_user.is_active:
        return render_template("settings.html", title="Settings", url=os.getenv("URL"))
    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


listNameArray = []


@login_required
@app.route("/userpage", methods=["POST", "GET"])
def userpage():
    global listNameArray

    if current_user.is_active:
        ## make dynamic for user logged in
        listNameArray = getListNames(current_user.user_id)

        listIds = getListIds(current_user.user_id)

        numItems = []

        # loop to match listname and match to id
        for entry in listIds:
            idList = getBusinessId(entry)
            num_of_items = len(idList)
            numItems.append(num_of_items)

        # print(list_id)

        return render_template(
            "userpage.html",
            title="My Account",
            url=os.getenv("URL"),
            names=listNameArray,
            num=numItems,
        )
    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


@login_required
@app.route("/create-newList", methods=["POST"])
def createNewList():
    if current_user.is_active:
        newList_name = request.form.get("newList")

        ## if the new list name != a list they current have, then create the new list
        if newList_name not in getListNames(current_user.user_id):
            createList(current_user.user_id, newList_name)
        else:
            print(f"{newList_name} already exists", flush=True)

        return '{"id":"%s","success":true}' % newList_name
    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


@login_required
@app.route("/list/<listName>", methods=["POST", "GET"])
def listpage(listName):
    if current_user.is_active:

        # get list of ids from the List table
        listIds = getListIds(current_user.user_id)
        liked_businesses = []

        # loop to match listname and match to id
        for entry in listNameArray:
            if entry == listName:
                index = listNameArray.index(entry)
                list_id = listIds[index]

                idList = getBusinessId(list_id)
                # print(idList)

                for id in idList:
                    ENDPOINT_YELPB = yelpBusinessInfo(id)
                    responseB = requests.get(url=ENDPOINT_YELPB, headers=HEADERS_YELP)
                    businessData = responseB.json()

                    # extract data from businessData to append to liked_businesses
                    # price currently doesn't pull from API - check later

                    id1 = businessData["id"]
                    name = businessData["name"]
                    picture = businessData["image_url"]
                    # price = businessData["price"]
                    rating = businessData["rating"]
                    # distance = businessData["distance"]
                    phone = businessData["display_phone"]
                    address = businessData["location"]["address1"]

                    new_data = {
                        "id": id1,
                        "name": name,
                        "picture": picture,
                        # "distance": int(distance) / 1000,
                        # "distance": distance,
                        # "price": price,
                        "rating": rating,
                        "phone": phone,
                        "address": address,
                    }

                    liked_businesses.append(new_data)

        return render_template(
            "listpage.html",
            title="My List",
            url=os.getenv("URL"),
            data={"liked_businesses": liked_businesses},
            name=listName,
        )
    else:
        print("No active user, redirect to login", flush=True)
        return redirect(url_for("login"), code=302)


@app.route("/register", methods=["GET", "POST"])
def register():
    # from .db import UserModel, db

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
            return (
                render_template("register.html", url=os.getenv("URL"), message=error),
                418,
            )
        elif not password:
            error = "Password is required."
            return (
                render_template("register.html", url=os.getenv("URL"), message=error),
                418,
            )

        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."
            return (
                render_template("register.html", url=os.getenv("URL"), message=error),
                418,
            )

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            createLikedList(new_user.user_id)
            # Return login page upon successful registration
            return render_template("login.html")
        else:
            return error, 418

    # Return a register page
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        # from .db import UserModel

        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
            return (
                render_template("login.html", url=os.getenv("URL"), message=error),
                418,
            )

        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
            return (
                render_template("login.html", url=os.getenv("URL"), message=error),
                418,
            )

        if error is None:

            # userId = user.user_id
            userId = UserModel.get_id(user)
            # Return home page upon successful registration, assuming it's "index.html"
            # if the above check passes, then we know the user has the right credentials
            login_user(user)
            user.is_active()
            print("User information:::", flush=True)
            print(current_user.user_id, flush=True)
            # return redirect(url_for('main.profile'))
            # return index()
            return redirect(url_for("userpage"), code=302)
        else:
            return error, 418

    # Return a login page
    return render_template("login.html")


@login_required
@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect("/")
    # return redirect(url_for('main.index'))


if __name__ == "__main__":
    app.run(debug=true)
