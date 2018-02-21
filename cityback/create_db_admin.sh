#!/bin/bash

# Base Script File (test/django_db/test.sh)
# Created: Fri 02 Feb 2018 15:38:55 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>

echo "This will delete the sqlite database do you want to proceed? (yes)"
read a
if [ "$a" != "yes" ]; then
  exit 0
fi

rm db.sqlite3
find -name migrations -exec rm -rf {} \;
python manage.py makemigrations
python manage.py makemigrations storage
python manage.py makemigrations scheduler
python manage.py makemigrations retrieval
python manage.py migrate

echo "creating admin user: admin/adminadmin"
echo "from django.contrib.auth.models import User; \
  User.objects.filter(email='admin@example.com').delete();\
  User.objects.create_superuser('admin', 'admin@example.com', 'adminadmin')" | \
  python manage.py shell


