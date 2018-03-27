#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e

python /app/cityback/manage.py collectstatic --noinput

mkdir -p /var/log/celery
cd /app/cityback
celery multi start beat \
      -A cityback --beat \
      --pidfile="/var/log/celery/%n.pid" \
      --logfile="/var/log/celery/%n.log"
# start web servers
nginx -g "daemon off;" > /var/log/nginx/access.log 2> /var/log/nginx/error.log

