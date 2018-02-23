#!/bin/bash

./redis_start.sh
mkdir -p /var/log/celery
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid" 
sleep .5
celery multi start worker1 \
    -A cityback --beat \
    --pidfile="/var/log/celery/%n.pid" \
    --logfile="/var/log/celery/%n.log"

python manage.py runserver 0.0.0.0:8000
#./daphne_run.sh
