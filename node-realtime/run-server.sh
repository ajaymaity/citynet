#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

path="$(dirname $(realpath $0))"

# echo $path

docker run --rm -it -p 3001:3001 -v "${path}/..":/app -w /app/node-realtime asegroup11/all_servers:citynet /bin/bash run.sh
