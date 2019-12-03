Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Your job is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. 
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, etc
  ├── error.log
  ├── forms.py *** The forms
  ├── models.py  *** The SQL Alchemy models
  ├── views.py *** The application views
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ├── migrations/ *** Folder containing details on database migrations
  ```

Overall:
* Models are located in `models.py`.
* Controllers are located in `views.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` --  Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `views.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` --  Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` --  Defines the forms used to create new artists, shows, and venues.
* `app.py` --  Initialises and creates the application, consolidating the models in `models.py` and controllers in `views.py`
* `views.py` --  Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* `models.py` --  Defines the data models that set up the database tables.
* `config.py` --  Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already. Secondly, [install and start postgres](https://classroom.udacity.com/nanodegrees/nd0044/parts/216c669c-5e62-43a1-bcb9-8a8e5eca972a/modules/43f34772-8032-4851-938b-d952bbfc7f1c/lessons/e9a00338-ff0d-415b-b382-25d445e529a1/concepts/5211128a-28f0-4e57-b181-ec28afb84ae6), if you haven't already. 

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Create a database called `fyyur` by running `psql -U postgres` and then `CREATE DATABASE fyyur;`. Exit by entering `\q`

4. Run the development server:
  ```
  $ FLASK_APP=app.py FLASK_ENV=development flask run
  ```

5. Navigate to Home page [http://localhost:5000](http://localhost:5000)
