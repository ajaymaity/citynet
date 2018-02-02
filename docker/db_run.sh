#!/bin/bash

# Base Script File (docker/run_db.sh)
# Created: Thu 01 Feb 2018 18:44:10 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}


path="$(dirname $(realpath $0))"


docker run --net host -P --rm -i -v db1:/etc/postgresql \
  -v db2:/var/log/postgresql -v db3:/var/lib/postgresql \
  -v "${path}/..":/app -w /app asegroup11/all_servers:citynet \
  /bin/bash /app/docker/db_run_cmd
