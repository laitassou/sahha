# Sahha Backend application

## Setup

Backend code goes into this repo.
The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:laitassou/sahha.git
$ cd sahha
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --python=python3.10 venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ python manage.py runserver
```
Collect the static files into STATIC_ROOT:
```sh
(venv)$ python manage.py collectstatic
```
And navigate to API Swagger Documentation `http://127.0.0.1:8000/swagger/`.

Redoc: `http://127.0.0.1:8000/redoc/`

## Walkthrough

Before you interact with the application, go to 
```sh
$ cd sahha_backend/
```
and create a local_settings.py to overwrite the settings and enviormental variables like local Database settings. 

sample `local_settings.py`
```sh
from .settings import *
import logging
    
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sahha',
        'USER': 'postgres',
        # 'PASSWORD': 'pass',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        # 'HOST': 'localhost',
        'PORT': 5432
    }
}
```

### Setup DB


```sh
sudo -u postgres psql

postgres=# create database sahha;
CREATE DATABASE
postgres=# create user postgres with encrypted password 'postgres';
CREATE ROLE
postgres=# grant all privileges on database sahha to postgres;
postgres=# ALTER ROLE postgres SUPERUSER;
```

### Django Admin

Creating an admin user
First we’ll need to create a user who can login to the admin site. Run the following command:

```sh
$ python manage.py createsuperuser
```

Enter your desired username and press enter.

```sh
Username: admin
```
You will then be prompted for your desired email address:

```sh
Email address: admin@example.com
```

The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.

```sh
Password: **********
Password (again): *********
Superuser created successfully.
```

Then go to `http://127.0.0.1:8000/admin/`. This is to
make sure you are redirected to django default admin panel where the DB can be managed and viewed.
Login with the credentials you created now.
