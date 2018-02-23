#!/bin/bash

celery multi stop worker1 --pidfile="/var/log/celery/%n.pid" 
celery -A cityback worker --beat
