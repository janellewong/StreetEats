# StreetEats

### What is it?
StreetEats is a website that allows users to access local restaurants based on their location. Users can register, login, connect with their friends by username, and customize lists of restaurants. Lists of restaurants are unique to each user to customize a title for their list and add restaurants to each of their lists. 

### Technologies Featured
- NginX as a reverse proxy
- Docker as a containerising service
- HTML and CSS for design of pages
- Flask and Python
- PostgreSQL Databases
- (3) APIs: YelpFusion API, IP address API, IP to coordinates API

### Main Features and Implementation
#### Registration and Login
Registration and login information are stored in a postgreSQL database to allow each user to have unique lists, friends, and account information. 

#### Connecting with Friends
Users can add friends to their friends lists. This action is facilitated by our User database of registered users, which is available to each user upon login. These friend connections are stored in another postgreSQL database. This friendship database forms a one-to-many relationship with our User database.

#### Restaurant Lists
Users are able to create new lists of restaurants to connect to their user profile, and add as many restaurants to any of their lists. The information for restaurants is pulled from the YelpFusion API and stored into a database, Restaurants. The title for the list of restaurants can then be added to a user's restaurant list, which connects the User database and Lists database. The Restaurants database the interacts with our Lists database, which is connected to a User database. These databases are postgreSQL databases.

### Database Schema
<img width="369" alt="DB Schema" src="https://user-images.githubusercontent.com/69429491/130236067-d19766b8-4670-429f-8449-c1caa5e773ee.png">

### Challenges and Solutions
Understanding how to connect our 3 APIs and our multiple databases was a challenge. We decided to divide API and database related tasks to assign to each team member. We had to stay organized and in communication to piece together our 3 APIs and our databases. We researched postgreSQL and API get/post requests in our assigned sections, and asked for help as needed.

### License
[MIT License](https://github.com/janellewong/StreetEats/blob/main/LICENSE)
