# Eat Until API

Django backend for the [Eat Until app](https://github.com/piRstone/eat-until-mobile).

### Stack

- Django
- Django Rest Framework
- PostgreSQL

## Installation

### Without Docker

Create a virtulenv with **python3**, source it then run `pip install -r requirements/dev.txt`.

Still in your virtuelenv, run `pre-commit install`.

Create a PostgreSQL database.

Copy the `eatuntil/settings/local.py.dist` file as `local.py` in the same directory and set your database settings in it then run the migrations with `./manage.py migrate`.

Launch the server with `./manage.py runserver 8000`;

### With Docker

Create a `docker-compose.override.yml` file to override default settings according to your preferences.

Then run `docker-compose up -d` to build and run db and django containers.

## Swagger

Swagger is available at `http://localhost:8000/swagger`.
