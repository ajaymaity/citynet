#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e

cd /app/cityback
rm -f celerybeat.pid
celery beat -A cityback
