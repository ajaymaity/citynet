#!/bin/bash

# Base Script File (build.sh)
# Created: Mon 29 Jan 2018 18:50:25 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Corentin Chéron <chronc@tcd.ie>

# --rm: remove image after run
# --net host copy host network connection
# -v bind host folder inside docker
# -w workdir inside the docker

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

realpath "$0"

path="$(dirname $(realpath $0))"

echo "creating volumes if absent"
docker volume create dm1
docker volume create db2
docker volume create db3
docker run --net host -P --rm -i -v db1:/etc/postgresql -v db2:/var/log/postgresql -v db3:/var/lib/postgresql -v "${path}/..":/app -w /app asegroup11/all_servers:citynet "$@"
