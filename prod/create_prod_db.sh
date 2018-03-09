#!/bin/bash

set -e
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD
source /app/config_private/bash_import_secret

echo "This will delete the current POSTGRESQL database!"
echo "Do you want to proceed? (yes)"
read a
if [ "$a" != "yes" ]; then
  exit 0
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
    createdb -O $PGUSER1 prod &&\
    echo "db created..." && \
psql -h localhost -p 5432 -U $PGUSER1 prod -c 'CREATE EXTENSION postgis;'
EOF

# do not remove existing migrations, they should be remove manually
# find /app/cityback/cityback -name migrations -type d -exec rm -rf "{}" +

python /app/cityback/manage.py makemigrations
python /app/cityback/manage.py migrate
echo "from django.contrib.auth.models import User; \
  User.objects.filter(email='admin@example.com').delete();\
  User.objects.create_superuser('$DJANGO_ADMIN', 'admin@example.com', '$DJANGO_PASSWORD')" | \
  python /app/cityback/manage.py shell
