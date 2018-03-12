#!/bin/bash

# Add or edit the following line in your postgresql.conf :
# listen_addresses = '*'
# Add the following line as the first line of pg_hba.conf. It allows access to all databases for all users with an encrypted password:
## TYPE DATABASE USER CIDR-ADDRESS  METHOD
#   host  all  all 0.0.0.0/0 md5

## Dumping data
# Change all METHOD to md5 -- not peer 
# Run --> PGPASSWORD=django psql -U django -d dev -f dump.sql 

# ----------------------------------------------

set -e

path=$(dirname $0)/..
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD
source $path/dev/db_source

echo "This will delete the current POSTGRESQL database!"
if [ "$1" != "--force" ]; then
  echo "Do you want to proceed? (yes)"
  read a
  if [ "$a" != "yes" ]; then
    exit 0
  fi
fi

# clear existing cluster
pg_dropcluster --stop 9.5 main

# create new one
pg_createcluster  9.5 main

# start db
service postgresql start

# create tmpdb
su postgres <<EOF
psql --command "CREATE USER $PGUSER1 WITH SUPERUSER PASSWORD '$PGPASSWORD' ;" &&\
    echo "User created..." && \
    createdb -O $PGUSER1 $PGDB &&\
    echo "db created..." && \
psql -h localhost -p 5432 -U $PGUSER1 $PGDB -c 'CREATE EXTENSION postgis;'
EOF

# do not remove existing migrations, they should be remove manually
# find /app/cityback/cityback -name migrations -type d -exec rm -rf "{}" +

python $path/cityback/manage.py makemigrations
python $path/cityback/manage.py migrate
echo "from django.contrib.auth.models import User; \
  User.objects.filter(email='admin@example.com').delete();\
  User.objects.create_superuser('$DJANGO_ADMIN', 'admin@example.com', '$DJANGO_PASSWORD')" | \
  python $path/cityback/manage.py shell
