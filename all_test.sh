#!/bin/bash
# Run all unit and integration tests.
# option from_docker to run the test from docker. This will skip
# the docker integration tests (docker/run_all_tests.sh)

set -e 
PRE="docker/run_inside_docker.sh bash -c"
if [ "$1" == "from_docker" ]; then
	PRE="bash -c"
fi
$PRE "cd cityback && python setup.py test"
echo "Running Django tests on SQlit DB"
$PRE "cd cityback && python manage.py test"
echo "Running Django tests on the POSTGRES DB"
$PRE "
  source config_private/bash_import_secret &&
  prod/create_prod_db.sh --force > /dev/null &&\
  cd cityback && \
  python manage.py test"
$PRE "cd frontend && npm install && npm run test-ci"
$PRE "cd node-realtime && npm install && npm run test-ci"
