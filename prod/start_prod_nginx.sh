#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e

python /app/cityback/manage.py collectstatic --noinput

# start web servers
nginx -g "daemon off;" > /var/log/nginx/access.log 2> /var/log/nginx/error.log

