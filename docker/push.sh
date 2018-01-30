#!/bin/bash

# Base Script File (build.sh)
# Created: Mon 29 Jan 2018 18:50:25 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>

# tag image
docker tag asegroup11/all_servers:citynet asegroup11/all_servers:citynet

# push image
docker push asegroup11/all_servers:citynet
