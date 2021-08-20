import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from flask import request


def api_location(ip):

    print(ip)

    ENDPOINT_LOC = f"https://ipinfo.io/{ip}?token=e5705a55652e77"  # method: GET
    response_loc = requests.get(url=ENDPOINT_LOC)
    print(response_loc)

    response_new = response_loc.json()["loc"].split(",")
    lat, long = response_new[0], response_new[1]

    return lat, long


def apiYelp():
    client_id = os.getenv("CLIENTID")
    API_KEY_YELP = os.getenv("APIKEYYELP")
    ENDPOINT_YELP = "https://api.yelp.com/v3/businesses/search"  # method: GET
    HEADERS_YELP = {"Authorization": "bearer %s" % API_KEY_YELP}

    return ENDPOINT_YELP, HEADERS_YELP


def yelpReviews(id):
    ENDPOINT_YELPR = f"https://api.yelp.com/v3/businesses/{id}/reviews"  # method GET

    return ENDPOINT_YELPR


def yelpBusinessInfo(id):
    ENDPOINT_YELPB = f"https://api.yelp.com/v3/businesses/{id}"  # method GET

    return ENDPOINT_YELPB
