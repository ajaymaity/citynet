#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

path="$(dirname $(realpath $0))"

# echo $path

docker run --rm -it -p 3000:3000 -v "${path}/..":/app -w /app/frontend asegroup11/all_servers:citynet npm install && /bin/bash run.sh start