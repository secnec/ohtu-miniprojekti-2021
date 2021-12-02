#!/bin/bash
# Tämä tiedosto on Github Actionsia varten,
# jottei robot testejä suoriteta Herokussa.

export DATABASE_URL
export SECRET_KEY

psql -h localhost -U postgres < schema.sql

poetry run flask run &

sleep 30

poetry run robot src/tests