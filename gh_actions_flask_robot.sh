#!/bin/bash
# Github Actionsia varten, jottei robot testejä suoriteta Herokussa.
export SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432
export SECRET_KEY=TEsT_KeY
# apt-get install --yes postgresql-client #chromium-chromedriver

psql -h localhost -U postgres < schema.sql
echo $SQLALCHEMY_DATABASE_URI

SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432 poetry run flask run &

sleep 30

poetry run robot src/tests