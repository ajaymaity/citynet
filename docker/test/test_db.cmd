#!/bin/bash

# Base Script File (test/test_db.sh)
# Created: Fri 02 Feb 2018 09:33:16 GMT
# Version: 1.0

source /app/docker/test/create_tmp_db.cmd

#

set -e
PGPASSWORD=docker psql -h localhost -p 5439 -U docker -c 'SELECT * FROM USER;'
PGPASSWORD=docker psql -h localhost -p 5439 -U docker -c 'SELECT PostGIS_version();'
ret=$?

source /app/docker/test/stop_db.cmd
exit $ret

