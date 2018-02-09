#!/bin/bash

# Base Script File (all_test.sh)
# Created: Fri 09 Feb 2018 12:45:29 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>

set -e 
docker/run_inside_docker.sh bash -c "cd backend; python setup.py test"
docker/run_inside_docker.sh bash -c "cd frontend; npm install && npm run test-ci"

