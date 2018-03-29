#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e
# copy all static files to /var/www/static (see django documentation)
python /app/cityback/manage.py collectstatic --noinput

# copy the nginx configuration file
cp /app/config_private/etc/nginx /etc/nginx/sites-enabled/default

# start web servers
nginx -g "daemon off;" > /var/log/nginx/access.log 2> /var/log/nginx/error.log

