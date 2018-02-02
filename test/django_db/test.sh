#!/bin/bash

# Base Script File (test/django_db/test.sh)
# Created: Fri 02 Feb 2018 15:38:55 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>


python test/django_db/manage.py makemigrations
python test/django_db/manage.py migrate

echo "from django.contrib.auth.models import User; \
  User.objects.filter(email='admin@example.com').delete();\
  User.objects.create_superuser('admin', 'admin@example.com', 'testadmin')" | \
  python test/django_db/manage.py shell

python test/django_db/manage.py runserver 0.0.0.0:8000 & PID2=$!
sleep 2.5


ret=$(wget localhost:8000 --timeout 2 -qO- | grep 'It worked!')
echo killing... $PID2
pkill -SIGTERM -P $PID2

if [ "$ret" != "" ]; then
  echo $ret
  exit 0
else
  exit -1
fi

