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

path="$(dirname $(realpath $0))"

# in dev mode, run the local image, dont download image from the server
if [ "$1" = "dev" ]; then
  shift
  echo "Running local docker image, when changes are validated, don't forget to push the image."
else
  docker pull asegroup11/all_servers:citynet
fi
#create volume if non existant
docker volume inspect db1 &>/dev/null || docker volume create db1
docker volume inspect db2 &>/dev/null || docker volume create db2
docker volume inspect db3 &>/dev/null || docker volume create db3
docker volume inspect nginx_conf &>/dev/null || docker volume create nginx_conf

docker run --hostname "cityback_dev" -p 443:443 -p 80:80 --rm -it -v db1:/etc/postgresql \
  -v db2:/var/log -v db3:/var/lib/postgresql \
  -v nginx_conf:/etc/nginx/ \
  -v "${path}/../../config_private_citynet/":/app/config_private/ \
 -v "${path}/..":/app -w /app asegroup11/all_servers:citynet "$@"
