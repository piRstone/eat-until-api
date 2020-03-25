# Eat Until API

## Installation

Create a virtulenv with **python3** and then run `pip install -r requirements/base.txt`.

Copy the `eatuntil/settings/local.py.dist` file as `local.py` in the same directory and set your database settings in it then run the migrations with `./manage.py migrate`.

Launch the server with `./manage.py runserver 8000`;

## Swagger

Swagger is available at `http://localhost:8000/swagger`.
