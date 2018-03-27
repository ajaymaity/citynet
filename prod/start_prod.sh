#!/bin/bash

if [ "$1" = "rds" ]; then
  source /app/config_private/bash_import_secret_aws
  service postgresql stop
elif [ "$1" = "local" ]; then
  source /app/config_private/bash_import_secret
  chown -R postgres /var/log/postgresql
  service postgresql restart
else
  echo "Please specify the db type:"
  echo "Usage $0 rds|local"
  exit
fi

set -e
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD

#create log directories
mkdir -p /var/log/celery /var/log/redis
chown -R redis /var/log/redis

# start db

# update django db (if needed)
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
daphne -p 8000 -b 127.0.0.1 cityback.asgi:application -v 1
echo "Stopping all servers"
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"

redis-cli shutdown
