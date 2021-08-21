# StreetEats


### Overview

StreetEats is a website that allows users to access local restaurants based on their location. Users can register, login, and customize lists of restaurants. Lists of restaurants are unique to each user to customize a title for their list and add/remove restaurants in each of their lists. 
Website Link:(https://street-eats.tech/)

The home page consists of a search bar where you enter the type of food and the location. If no location is entered then the user's location is utilized. The navigation bar has links to the Login and Register page.

<img width="1000" alt="Screen Shot 2021-08-20 at 12 57 55 PM" src="https://user-images.githubusercontent.com/38405709/130287628-78beb3e5-c926-4b28-af14-d35b6847e0fe.png">

Once the search command has been processed restaurants at that location that provide the cuisine are displayed.

<img width="1429" alt="Screen Shot 2021-08-20 at 12 58 31 PM" src="https://user-images.githubusercontent.com/38405709/130298868-65c92fb8-0f16-4063-9816-c6e03b6c02ae.png">

Your favourite restaurants can be added to a personal list and saved.

<img width="1436" alt="Screen Shot 2021-08-20 at 1 00 10 PM" src="https://user-images.githubusercontent.com/38405709/130299551-a343d4f2-31ae-465a-8d81-5b554273e0ca.png">

<img width="1437" alt="Screen Shot 2021-08-20 at 1 00 47 PM" src="https://user-images.githubusercontent.com/38405709/130299569-5383372f-8caa-4060-96a0-ee079eb068ba.png">

You can search for locations without logging in *however*, you cannot make your personalised lists.

---

### Getting Started

This example uses features in Docker 3.3. 2. Install this version to run.

To run the website as an application use:
```docker-compose up --build``` 

---

### Main Features and Implementation

#### Registration and Login
Registration and login information is stored in a postgreSQL database to allow each user to have unique lists and account information. 

#### Restaurant Lists
Users are able to create new lists of restaurants to connect to their user profile, and add/remove as many restaurants to any of their lists. The information for restaurants is pulled from the YelpFusion API and stored into a database, Restaurants. The title for the list of restaurants can then be added/removed in a user's restaurant list, which connects the User database and Lists database. The Restaurants database the interacts with our Lists database, which is connected to a User database. These databases are postgreSQL databases.

---
### Technologies Featured

- NginX as a reverse proxy
- Docker as a containerising service
- HTML and CSS for design of pages
- Flask and Python
- PostgreSQL Databases
- Docker
- Prometheus
- Grafana

#### APIs:
- YelpFusion API
-  IP address API
- IP to coordinates API

---
### Database Schema

We're making use of 4 databases here: users, lists, businesses and listcontents
- The user_id key from the from the users table is used as a foreign key in the lists table enabling each user to have their set of restaurant lists.
- The table listcontents which stores the data of each user's personalised lists has the primary key list_id_fk and foreign key businesses_id_fk.
- Tables users and lists have one to many relationships with lists, businesses and listcontents respectively.

---
### Docker  Containers in the Instance

- StreetEats
- PostgreSql 
- Nginx-Certbot

---
### Monitoring

This project is being monitored through a combination of the tools

- cAdvisor (Port 8080)
- Prometheus (Port 9090)
- Grafana(Port 3000)

---
### CI/CD

Both CI and CD workflows are automated.

---
### Testing

A linter check over the code occurs when someone makes a pull request to ensure optimal execution at all points.

---
### Challenges and Solutions

Understanding how to connect our 3 APIs and our multiple databases was a challenge. We decided to divide API and database related tasks to assign to each team member. We had to stay organized and in communication to piece together our 3 APIs and our databases. We researched postgreSQL and API get/post requests in our assigned sections, and asked for help as needed.

---
### Contributors

- Ayesha (https://github.com/ayesha133)
- Janelle (https://github.com/janellewong)
- Joey (https://github.com/aHappyCamer)
- Nandhini (https://github.com/nandhiniswaminathan)
- Rinki (https://github.com/mamnuya)

---
### License

[MIT License](https://github.com/janellewong/StreetEats/blob/main/LICENSE)
