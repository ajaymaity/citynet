#!/bin/bash

# Base Script File (test/test_db.sh)
# Created: Fri 02 Feb 2018 09:33:16 GMT
# Version: 1.0
#

# from https://docs.djangoproject.com/en/2.0/intro/tutorial01/

source /app/docker/test/create_tmp_db.cmd

python docker/test/django_db/manage.py runserver 0.0.0.0:8000 &>/dev/null & PID2=$!
sleep 1.5

ret=$(wget localhost:8000 --timeout 2 -qO- | grep 'It worked!')

# stopping django server
pkill -SIGINT -P $PID2

# stopping postgres server
source /app/docker/test/stop_db.cmd

if [ "$ret" != "" ]; then
  echo $ret
  exit 0
else
  exit -1
fi

exit $ret
