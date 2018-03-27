#!/bin/bash

source /app/config_private/bash_import_secret_aws
set -e

#create log directories
mkdir -p /var/log/celery /var/log/redis
chown -R redis /var/log/redis

# update django db (if needed)
python /app/cityback/manage.py migrate

# message routers
service redis-server restart

cd /app/cityback
# celery tasks
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"
sleep .2
# TODO put inside a service file, see http://docs.celeryproject.org/en/latest/userguide/daemonizing.html
celery multi start worker1 \
    -A cityback \
    --pidfile="/var/log/celery/%n.pid" \
    --logfile="/var/log/celery/%n.log"

# daphne start here
daphne -p 8000 -b 0.0.0.0 cityback.asgi:application -v 1

echo "Stopping all servers"
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"

redis-cli shutdown
