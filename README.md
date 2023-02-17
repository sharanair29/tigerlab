This app uses django rest framework to import csv files into the TeamScore Model on the backend. It is utilizing a postgres backend as well as a redis server to implement caching. It is also using HTMX for forms that enable team score objects to be added, edited and deleted. The front end utilizes bootstrap 5.

Below are the links to the documentation that was referred to in implementing this webapp:

HTMX for forms : https://htmx.org/
redis for caching : https://redis.io/

# HTMX

HTMX forms were implemented instead of standard Crispy forms to utilize immediate page updates without any refreshes using just HTML and minimal javascript instead of writing custom AJAX, Websockets or Server Event scripts.


# Redis

To start the webapp, please have a redis server runnning and check your port connection to make sure it matches with the configurations on the settings.py file under the Cache section.
If you are on a mac you can use homebrew and run:

brew install redis
brew services start redis

Test your connection by keying in PING, you should receive PONG as an output.

# Postgres

All sensitive information such as database password, secret keys and allowed hosts has been decoupled using python-decouple. These are stored in the .env file. Attached to this repository is a sample .env.example file, please rename this file to a .env file with your db parameters, secret key and allowed hosts.

# To start the application

Once redis is running, and a postgres db, db username and db password has been set up. Clone the repository and update the .env file with the appropriate settings, if you are in need of generating a secret key for the django web app you may retrieve one from : https://miniwebtool.com/django-secret-key-generator/

# Virtual environment setup 

Create a python3 virtual environment in the root directory of the application, it is best to stick to the root directory as when this application is pushed to the production or staging server and is utilizing the Jenkinsfile for automated deployments, it is configured to look for the python virtual environment in the root directory (or you may choose to update this).

To create a virtual environment and activate it on a Mac:

python3 -m venv ./venv

source ./venv/bin/activate

Once your virtual environment has been activated you may install all libraries and dependencies for this application from the requirements.txt file. 

pip install -r requirements.txt

# Static files

To ensure that your static files are collected and a static folder is created in the root of your application run:

python manage.py collectstatic

When prompted key in Y for "Yes"

You should see a static folder in the root of your local repository

# Run migrations

Next, run all migrations to ensure your tables are created in the database which you connected to using your .env file setup.

python manage.py makemigrations

python manage.py migrate

# Run app

You may now run:

python manage.py runserver

Hit Ctrl + C to stop your server from running the application locally.

In case you would like to get a view of how the application works from a mobile device or an ipad. You may choose the run application on your ip address at port 8000.

On a mac get your ip address by running: 

ipconfig getifaddr en0

You should get your public IP address in this format : 

190.16x.7x.1xx

Now run the following command on your IP address at port 8000:

python manage.py runserver 190.16x.7x.1xx:8000

Your phone or ipad should be connected to the same internet your laptop is connected to. You may view the app on your mobile browser using this link:

190.16x.7x.1xx:8000

# Logging

This application also uses Python's default basicConfig logging, to log events for the API. You can find these outputs in the logging.log file generated.
Refer to this for tracebacks should there be any errors with the core API to import CSV files.

# Tests

To run tests:

python manage.py test

Logging is also implemented for tests, the output can be found in testing.log.





