#!/bin/bash
# Github Actionsia varten, jottei robot testejä suoriteta Herokussa.
export SQLALCHEMY_DATABASE_URI=$1
export SECRET_KEY=$2
# apt-get install --yes postgresql-client #chromium-chromedriver

psql -h localhost -U postgres < schema.sql
echo $SQLALCHEMY_DATABASE_URI
poetry run flask run &

sleep 30

poetry run robot src/tests