#!/bin/bash

# Base Script File (test/test_db.sh)
# Created: Fri 02 Feb 2018 09:33:16 GMT
# Version: 1.0
#
error() {
    echo -e  "\e[41mERROR in test file $2"'!'"\e[0m"
  exit -1
}

trap 'error $LINENO $(basename $i)' ERR

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

path="$(dirname $(realpath $0))"
root=${path}/..

echo -e "\n********** RUNNING DOCKER TESTS **********"
for i in $path/test/test_*.cmd; do
  echo Running inside ephemeral docker $(basename $i)
  $path/test/ephemeral_run.sh /bin/bash /app/docker/test/$(basename $i)
done

echo -e  '\e[42mAll docker tests succeeded!\e[0m'
exit
fi
