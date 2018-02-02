#!/bin/bash

# Base Script File (test/test_db.sh)
# Created: Fri 02 Feb 2018 09:33:16 GMT
# Version: 1.0
#

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
path="$(dirname $(realpath $0))"
root=${path}/../..

$root/docker/db_run.sh & PID=$!

sleep 3

$root/docker/run_inside_docker.sh /bin/bash test/django_db/test.sh
ret=$?


pkill -SIGTERM -P $PID
sleep 1.5

if [ $ret -eq 0 ]; then
  echo  -e '\e[42mDjango test succeed!\e[0m'
  exit 0
else
  echo -e "\e[41mERROR django not working\e[0m"
  exit -1
fi


exit $ret

