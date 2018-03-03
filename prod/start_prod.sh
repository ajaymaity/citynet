#!/bin/bash

set -e
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD
source /app/config_private/bash_import_secret

#create log directories
mkdir -p /var/log/celery /var/log/redis
chown -R redis /var/log/redis
chown -R postgres /var/log/postgresql

# start db
service postgresql restart

# update django db (if needed)
python /app/cityback/manage.py makemigrations
python /app/cityback/manage.py makemigrations storage
python /app/cityback/manage.py makemigrations scheduler
python /app/cityback/manage.py makemigrations retrieval
python /app/cityback/manage.py makemigrations dashboard
python /app/cityback/manage.py migrate
python /app/cityback/manage.py collectstatic --noinput

# message routers
service redis-server restart

cd /app/cityback
# celery tasks
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"
sleep .2
# TODO put inside a service file, see http://docs.celeryproject.org/en/latest/userguide/daemonizing.html
celery multi start worker1 \
    -A cityback --beat \
    --pidfile="/var/log/celery/%n.pid" \
    --logfile="/var/log/celery/%n.log"

# start web servers
service nginx restart

# daphne start here
#python manage.py runworker????
daphne -p 8000 -b 127.0.0.1 cityback.asgi:application -v 1
echo "Stopping all servers"
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"

redis-cli shutdown
