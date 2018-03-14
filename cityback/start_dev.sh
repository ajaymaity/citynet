#!/bin/bash

# start postgresql server
service postgresql start

# message routers
service redis-server start
./manage.py makemigrations
./manage.py migrate

# celery tasks
mkdir -p /var/log/celery
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"
sleep .2
celery multi start worker1 \
    -A cityback --beat \
    --pidfile="/var/log/celery/%n.pid" \
    --logfile="/var/log/celery/%n.log"

# daphne start here, django runserver fails somehow
python manage.py runserver 0.0.0.0:8000 -v 1
#daphne -p 8000 -b 0.0.0.0 cityback.asgi:application -v 1
echo "Stopping all servers"
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"

redis-cli shutdown
#service rabbitmq-server stop

