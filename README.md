# MazeoSocketChat
Group chat with Django Channels and websocket
## This project has been written based on Turkish language, other features and languages will be added.

## Installation

python manage.py collectstatic

python manage.py migrate 

## open settings.py and set your redis configuration

## After that it's time to (make) up your redis server
example:

docker run -p 5000:5000 -d redis:5

or 

redis-server

python manage.py runserver 0.0.0.0:8000

## Add superuser: 

python manage.py createsuperuser

--Other users can signup through the interface

## Finally you need to add chat from admin panel 

# ENJOY!
