#!/bin/bash
# Run all unit and integration tests.
# option from_docker to run the test from docker. This will skip
# the docker integration tests (docker/run_all_tests.sh)

set -e 
PRE="docker/run_inside_docker.sh bash -c"
if [ "$1" == "from_docker" ]; then
	PRE="bash -c"
else
	docker/run_all_tests.sh
fi
$PRE "cd backend && python setup.py test"
$PRE "cd frontend && npm install && npm run test-ci"
$PRE "cd node-realtime && npm install && npm run test-ci"

