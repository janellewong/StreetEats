from flask import Flask, g
from flask import session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from . import app
from flask_login import UserMixin

db = SQLAlchemy(app)
# migrate = Migrate(app, db)

friends = db.Table('friends',
    db.Column("user_id_fk", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("friend_id_fk", db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
)

# create user table
class UserModel(db.Model, UserMixin):
    __tablename__ = "users"
    # Add user id, username, password columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    lists = db.relationship("Lists", backref="List_OwnerID")

    #User has lists that refers to Lists db
    friendship = db.relationship("UserModel",
                    secondary=friends,
                    primaryjoin=user_id==friends.c.user_id_fk,
                    secondaryjoin=user_id==friends.c.friend_id_fk,
                    backref="followed_by"
    )

    def __init__(self, user_id, username, password):
        self.user_id = user_id
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
    db.Column("list_id_fk", db.Integer, db.ForeignKey("lists.list_id")),
    db.Column("business_id_fk", db.String, db.ForeignKey("businesses.business_id")),
)

class Lists(db.Model):
    __tablename__ = "lists"
    # Add id number of user who owns list, name of list, list_id number columns
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String())
    user_id_fk = db.Column(db.Integer, db.ForeignKey("users.user_id"))
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


# class FriendModel(db.Model):
#     ___tablename___ = "friends"

#     user_id_fk = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

load_dotenv()
db.create_all()
