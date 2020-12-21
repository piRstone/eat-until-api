FROM python:3

ENV PYTHONBUFFERED=1

# RUN apt-get update && apt-get install --yes binutils libproj-dev gdal-bin postgis

WORKDIR /srv/eatuntil

COPY requirements/base.txt /srv/eatuntil/
COPY requirements/dev.txt /srv/eatuntil/

RUN pip install -r dev.txt

COPY . /srv/eatuntil/
