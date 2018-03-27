#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e

python /app/cityback/manage.py collectstatic --noinput

ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

# start web servers
nginx -g "daemon off;"

