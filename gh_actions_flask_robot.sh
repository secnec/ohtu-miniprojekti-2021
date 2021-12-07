#!/bin/bash
# Tämä tiedosto on Github Actionsia varten,
# jottei robot testejä suoriteta Herokussa.

# Jotta aliprosessit näkevät muuttujat:
export DATABASE_URL
export SECRET_KEY

# Lisää taulut tietokantaan
psql -h localhost -U postgres < schema.sql

# Flask suoritetaan taustalla
poetry run flask run &

sleep 30

poetry run robot src/tests

kill $(jobs -p)