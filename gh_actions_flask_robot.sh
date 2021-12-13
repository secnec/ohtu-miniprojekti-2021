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

until curl -s -f -o /dev/null 127.0.0.1:5000
do
    sleep 3
done

poetry run robot tips_app/tests
value=$?

kill $(jobs -p)

exit $value