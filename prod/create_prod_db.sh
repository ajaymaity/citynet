#!/bin/bash

set -e

if [ "$1" == "" ]; then
    echo "Creating empty database"
else
    echo "Importing db from $1"
fi
path=$(dirname $0)/..
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD
source $path/config_private/bash_import_secret

echo "This will delete the current POSTGRESQL database!"
if [ "$1" != "--force" ]; then
  echo "Do you want to proceed? (yes)"
  read a
  if [ "$a" != "yes" ]; then
    exit 0
  fi
else
  shift
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

#import the database
if [ "$1" != "" ]; then
    echo "Importing database $1"

su postgres <<EOF
    psql -d $PGDB -f $1
    psql --command "alter user $PGUSER1 with superuser password '$PGPASSWORD' ;"
EOF
fi
# do not remove existing migrations, they should be remove manually
# find /app/cityback/cityback -name migrations -type d -exec rm -rf "{}" +

python $path/cityback/manage.py migrate
echo "from django.contrib.auth.models import User; \
  User.objects.filter(email='admin@example.com').delete();\
  User.objects.create_superuser('$DJANGO_ADMIN', 'admin@example.com', '$DJANGO_PASSWORD')" | \
  python $path/cityback/manage.py shell
