#!/bin/bash
# Base Script File (demo.sh)

path=$(dirname $0)
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD
source $path/config_private/bash_import_secret

cd cityback
#reset the DB

# start all the servers in dev mode
./start_dev.sh