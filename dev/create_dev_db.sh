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

if [ "$1" == "" ]; then
    echo "Creating empty database"
else
    echo "Importing db from $1"
fi

path=$(dirname $0)/..
source $path/prod/create_prod_db.sh

# allow postgresql acces from outside

pgconf="/etc/postgresql/9.5/main/pg_hba.conf"
pgconf2="/etc/postgresql/9.5/main/postgresql.conf"
if [ "`tail -1 ${pgconf} | cut -c 1`" == "#" ]; then
 echo "host  all  all 0.0.0.0/0 md5" >> ${pgconf}
fi
echo "listen_addresses = '*'" >> $pgconf2

#import the database
if [ "$1" != "" ]; then
    echo "Importing database $1"
su postgres <<EOF
    psql -d $PGDB -f $1
    psql --command "alter user $PGUSER1 with superuser password '$PGPASSWORD' ;"
EOF
fi

service postgresql restart

python $path/cityback/manage.py makemigrations
python $path/cityback/manage.py migrate
echo "from django.contrib.auth.models import User; \
  User.objects.filter(email='admin@example.com').delete();\
  User.objects.create_superuser('$DJANGO_ADMIN', 'admin@example.com', '$DJANGO_PASSWORD')" | \
  python $path/cityback/manage.py shell
