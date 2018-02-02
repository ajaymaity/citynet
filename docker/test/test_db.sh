#!/bin/bash

# Base Script File (test/test_db.sh)
# Created: Fri 02 Feb 2018 09:33:16 GMT
# Version: 1.0
#

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
path="$(dirname $(realpath $0))"
root=${path}/../..

$root/docker/db_run.sh & PID=$!

sleep 5

$root/docker/run_inside_docker.sh \
  /bin/bash -c "PGPASSWORD=docker psql -h localhost -p 5432 -U docker -c 'SELECT * FROM USER;'"

$root/docker/run_inside_docker.sh \
  /bin/bash -c "PGPASSWORD=docker psql -h localhost -p 5432 -U docker -c 'CREATE EXTENSION postgis;'"
$root/docker/run_inside_docker.sh \
  /bin/bash -c "PGPASSWORD=docker psql -h localhost -p 5432 -U docker -c 'SELECT PostGIS_version();'"
ret=$?
pkill -SIGTERM -P $PID
sleep 2

if [ $ret -eq 0 ]; then
  echo "Db is working."
else
  echo "ERROR, DB is down."
fi
exit $ret

