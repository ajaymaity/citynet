#!/bin/bash

source /app/config_private/bash_import_secret_aws

set -e

cd /app/cityback
celery beat -A cityback
      

