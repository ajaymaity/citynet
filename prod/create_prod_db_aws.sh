#!/bin/bash


if [ "$1" == "" ]; then
    echo "Creating empty database"
else
    echo "Importing db from $1"
fi
path=$(dirname $0)/..
# import PGUSER PGPASSWORD DJANGO_ADMIN DJANGO_PASSWORD
source $path/config_private/bash_import_secret_aws

echo "This will delete the current POSTGRESQL database!"
if [ "$1" != "--force" ]; then
  echo "Do you want to proceed? (yes)"
  read a
  if [ "$a" != "yes" ]; then
    exit 0
  fi
fi


psql -U $PGUSER1  postgres --command "DROP DATABASE $PGDB;"
# create tmpdb
psql -U dbmaster -W postgres --command "DROP ROLE IF EXISTS $PGUSER1;CREATE USER $PGUSER1 WITH PASSWORD '$PGPASSWORD'; \
grant rds_superuser to $PGUSER1; \
alter user $PGUSER1 with createdb;"
psql -U $PGUSER1 template1 --command "CREATE DATABASE $PGDB;" 
echo "db created..."
psql -U $PGUSER1 $PGDB -c '
CREATE EXTENSION postgis;
create extension fuzzystrmatch;
create extension postgis_tiger_geocoder;
create extension postgis_topology;
alter schema tiger owner to rds_superuser; 
alter schema tiger_data owner to rds_superuser;
alter schema topology owner to rds_superuser;
CREATE FUNCTION exec(text) returns text language plpgsql volatile AS $f$ BEGIN EXECUTE $1; RETURN $1; END; $f$;'
psql -U $PGUSER1 $PGDB -c "      
SELECT exec('ALTER TABLE ' || quote_ident(s.nspname) || '.' || quote_ident(s.relname) || ' OWNER TO rds_superuser;')
  FROM (
    SELECT nspname, relname
    FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid) 
    WHERE nspname in ('tiger','topology') AND
    relkind IN ('r','S','v') ORDER BY relkind = 'S')
s;"
  

#import the database
if [ "$1" != "" ]; then
    echo "Importing database $1"

    psql -U $PGUSER1 -d $PGDB -f $1
fi
