# Project: Temporal
Private server for DRAGON BALL: THE BREAKERS, made by BreadandYeast.

Currently lobby only.

## Dev Setup

```
python -m venv venv
# mac/linux
source venv/bin/activate
# windows
./venv/scripts/activate.ps1

pip install -r requirements.txt
cp default.env .env
python manage.py runserver
```

## Setup for HTTPS

replace `runserver` line with:

```
hypercorn --bind 127.0.0.1:443 --certfile test.crt --keyfile test.key breadbreaker.asgi:application --keep-alive 10
```
