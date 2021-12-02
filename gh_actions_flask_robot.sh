#!/bin/bash
# Github Actionsia varten, jottei robot testejä suoriteta Herokussa.
apt-get update
# apt-get install --yes postgresql-client #chromium-chromedriver

psql -h localhost -U postgres < schema.sql

poetry run flask run &

sleep 30

poetry run robot src/tests