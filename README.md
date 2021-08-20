# StreetEats



### What is it?
StreetEats is a website that allows users to access local restaurants based on their location. Users can register, login, connect with their friends by username, and customize lists of restaurants. Lists of restaurants are unique to each user to customize a title for their list and add/remove restaurants in each of their lists. 
Website Link:(https://street-eats.tech/)

<img width="1000" alt="Screen Shot 2021-08-20 at 12 57 55 PM" src="https://user-images.githubusercontent.com/38405709/130287628-78beb3e5-c926-4b28-af14-d35b6847e0fe.png">
<img width="750" alt="Screen Shot 2021-08-20 at 12 58 31 PM" src="https://user-images.githubusercontent.com/38405709/130287669-df8fd070-3524-40a3-a6c1-2780c246e16e.png">
<img width="750" alt="Screen Shot 2021-08-20 at 1 00 10 PM" src="https://user-images.githubusercontent.com/38405709/130287686-d2e0c4d2-5f26-4c43-8539-f19ab418d339.png">
<img width="750" alt="Screen Shot 2021-08-20 at 1 00 47 PM" src="https://user-images.githubusercontent.com/38405709/130287697-13159601-23d3-45c2-8d3c-7a95766e9f36.png">


---


### Requirements
This example uses features in Docker 3.3. 2. Install this version to run.

### Run as an application
To run the website as an application:
```docker-compose up --build``` 

---


### Technologies Featured
- NginX as a reverse proxy
- Docker as a containerising service
- HTML and CSS for design of pages
- Flask and Python
- PostgreSQL Databases
- (3) APIs: YelpFusion API, IP address API, IP to coordinates API
---


### Main Features and Implementation
#### Registration and Login
Registration and login information are stored in a postgreSQL database to allow each user to have unique lists, friends, and account information. 

#### Connecting with Friends
Users can add friends to their friends lists. This action is facilitated by our User database of registered users, which is available to each user upon login. These friend connections are stored in another postgreSQL database. This friendship database forms a one-to-many relationship with our User database.

#### Restaurant Lists
Users are able to create new lists of restaurants to connect to their user profile, and add/remove as many restaurants to any of their lists. The information for restaurants is pulled from the YelpFusion API and stored into a database, Restaurants. The title for the list of restaurants can then be added/removed in a user's restaurant list, which connects the User database and Lists database. The Restaurants database the interacts with our Lists database, which is connected to a User database. These databases are postgreSQL databases.

---
### Database Schema
<img width="369" alt="DB Schema" src="https://user-images.githubusercontent.com/69429491/130236067-d19766b8-4670-429f-8449-c1caa5e773ee.png">

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
