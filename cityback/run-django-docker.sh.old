#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

path="$(dirname $(realpath $0))"

# echo $path

docker run --rm -it -p 8000:8000 -v "${path}/..":/app -w /app/cityback asegroup11/all_servers:citynet /bin/bash create_db_admin.sh