#!/bin/bash

source /app/config_private/bash_import_secret_aws
set -e

#create log directories
mkdir -p /var/log/celery /var/log/redis
chown -R redis /var/log/redis

# update django db (if needed)
python /app/cityback/manage.py migrate

# message routers
service redis-server start

if ls /var/log/celery/*pid 1> /dev/null 2>&1; then
  rm -f /var/log/celery/*pid
fi
cd /app/cityback
# celery tasks
# TODO put inside a service file, see http://docs.celeryproject.org/en/latest/userguide/daemonizing.html
celery multi start worker1 \
    -A cityback --beat \
    --pidfile="/var/log/celery/%n.pid" \
    --logfile="/var/log/celery/%n.log"

# daphne start here
daphne -p 8000 -b 0.0.0.0 cityback.asgi:application -v 2

echo "Stopping all servers"
celery multi stop worker1 --pidfile="/var/log/celery/%n.pid"

redis-cli shutdown
