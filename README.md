# Baggy Soap Website Local Setup

A brief setup to get the Baggy Soap website running locally.
Please note, this readme is written for Linux and needs updating if
you want to use a Mac.

## Requirements

- Python (v3.6.x) / pip / virtualenv / virtualenvwrapper
- Postgres

## Installing requirements

1) Install Python 3.6.4

```
$ sudo apt-get install build-essential checkinstall
$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
$ cd /usr/src
$ sudo wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
$ sudo tar xzf Python-3.6.4.tgz
$ cd Python-3.6.4
$ sudo ./configure --enable-optimizations
$ sudo make altinstall
```

2) Install virtualenvwrapper and make virtualenv

```
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenvwrapper
```

Add to .bashrc

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/workspace
source /usr/local/bin/virtualenvwrapper.sh
```

Reload shell startup file:

```
$ source ~/.bashrc
```

Make virtualenv:

```
$ mkvirtualenv --python=python3 baggy-soap
```

3) Set up PostgreSQL database

Install new version: 

https://www.postgresql.org/download/linux/ubuntu/

Create user and DB:

```
$ sudo su - postgres
$ psql
# CREATE USER baggysoapdb WITH PASSWORD 'khAk8ZTguB4zS3';
# CREATE DATABASE baggysoap;
# GRANT ALL PRIVILEGES ON DATABASE baggysoap to baggysoapdb;
# \q
$ exit
```

## Installation

To install this project, follow these steps:

```
$ git clone https://github.com/baggy-soap/baggy-soap.git
$ cd baggy-soap/
$ pip3 install -r requirements.txt
$ cp .env.example .env
$ python manage.py migrate
```

To create yourself as an admin user on the Django website, do the following:

```
$ python manage.py createsuperuser
```

Choose a username and password, and use your baggysoap.co.uk email address.

## Running Locally

```
$ workon baggy-soap
$ python manage.py runserver
```

Go to http://127.0.0.1:8000 to verify the website is running, 
and http://127.0.0.1:8000/admin to test your login credentials.

## Running Tests

Currently all tests are nested under the "tests/" directory and mimics the current folder structure.
The virtualenv needs to be enabled before running the tests.

    $ python manage.py test -v 2

**N.B.** You might need to give the db user `baggysoapdb` permission to create databases so that it can create the test database:

```
$ sudo su - postgres
$ psqsl
# ALTER USER zegodb CREATEDB;
# \q
$ exit
```

## Adding and upgrading Python dependencies

We use [`pip-tools`](https://github.com/jazzband/pip-tools) to manage Python dependencies.

To add a new direct dependency, add it to `requirements.in` and run `pip-compile requirements.txt` will be recreated, pinning an exact version of the new package and all its dependencies.

To upgrade a particular package to the latest, you can run (for example) `pip-compile -P celery`
to regenerate a new `requirements.txt` with the latest package and valid dependencies while leaving
other packages at their current versions!
