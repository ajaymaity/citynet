#!/bin/bash

# Base Script File (build.sh)
# Created: Mon 29 Jan 2018 18:50:25 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>



docker image build . --network host -t citynet

#unit test

docker run --net host citynet bash /root/dockertest.sh
