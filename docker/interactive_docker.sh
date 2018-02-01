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
# -i interactive
# -t open a terminal (BASH for our image)

path="$(dirname `realpath -m $0`)"
docker run --net host -it -v "${path}/..":/app -w /app asegroup11/all_servers:citynet 
