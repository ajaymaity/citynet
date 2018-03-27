#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e
mkdir -p /var/log/celery /var/log/redis
service redis-server start

python /app/cityback/manage.py collectstatic --noinput

if ls /var/log/celery/*pid 1> /dev/null 2>&1; then
  rm -f /var/log/celery/*pid
fi

cd /app/cityback
celery multi start beat \
      -A cityback --beat \
      --pidfile="/var/log/celery/%n.pid" \
      --logfile="/var/log/celery/%n.log"
# start web servers
nginx -g "daemon off;" > /var/log/nginx/access.log 2> /var/log/nginx/error.log

