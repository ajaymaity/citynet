#!/bin/bash

# Base Script File (build.sh)
# Created: Mon 29 Jan 2018 18:50:25 GMT
# Version: 1.0

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
docker volume inspect db1_dev &>/dev/null || docker volume create db1_dev
docker volume inspect db2_dev &>/dev/null || docker volume create db2_dev
docker volume inspect db3_dev &>/dev/null || docker volume create db3_dev

if [ $# -gt 0 ] ; then
  exec="-c '$@'"
else
  exec=""
fi

docker run -p 5432:5432 -p 8000:8000 --rm -it --name citynet --hostname dev_docker \
  -v db1_dev:/etc/postgresql \
  -v db2_dev:/var/log \
  -v db3_dev:/var/lib/postgresql \
  -v "${path}/..":/app -w /app asegroup11/all_servers:citynet \
  bash -c "source  /app/config_private/bash_import_secret; \
   service postgresql start; /bin/bash $exec"
