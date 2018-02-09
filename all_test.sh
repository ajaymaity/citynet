#!/bin/bash
# Run all unit and integration tests.
# option from_docker to run the test from docker. This will skip
# the docker integration tests (docker/run_all_tests.sh)

set -e 
if [ "$1" == "from_docker" ]; then
  (cd backend && python setup.py test)
  (cd frontend && npm install && npm run test-ci)
else
  docker/run_all_tests.sh
  docker/run_inside_docker.sh bash -c "cd backend; python setup.py test"
  docker/run_inside_docker.sh bash -c "cd frontend; npm install && npm run test-ci"
fi
