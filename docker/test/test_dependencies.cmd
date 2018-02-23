error() {
   echo "ERROR in DOCKER UNIT TEST on line $1 !!!!!!"  > /dev/stderr
   exit -1
  }
trap 'error $LINENO' ERR


# Timezone
[ "`cat /etc/timezone`" == "Europe/Dublin" ]

# PostGreSQL
[ "`psql --version`" == 'psql (PostgreSQL) 9.5.11' ]
/etc/init.d/postgresql start && sleep 2
[ "`/etc/init.d/postgresql status | cut -d'(' -f 2 | cut -d')' -f 1 | cut -c 6-`" \
  == "5432" ]

# node js
[ "`npm --version`" == '5.6.0' ]

# these test are now in the javascript tests and not install in the docker image
# mapbox
#[ "`npm -g list 2>/dev/null | grep "mapbox-gl" | head -1 | cut -d'@' -f 2`" == "0.44.0" ]
# eslint
#[ "`npm -g list 2>/dev/null | grep "eslint" | head -1 | cut -d'@' -f 2`" == "4.16.0" ]

# python versions
python --version
[ `python --version | cut -d' ' -f2` == "3.5.2" ]
python -c "print('Hello World')"
[ "`python -c "import django; print(django.__version__)"`" == "2.0.2" ]
[ "`python -c "import redis; print(redis.__version__)"`" == "2.10.6" ]
[ "`python -c "import celery; print(celery.__version__)"`" == "4.1.0" ]
[ "`python -c "import psycopg2; print(psycopg2.__version__)"`" == "2.7.3.2 (dt dec pq3 ext lo64)" ]
[ "`python -c "import oauth2client; print(oauth2client.__version__)"`" == "4.1.2" ]
[ "`python -c "import geojson; print(geojson.__version__)"`" == "2.3.0" ]
[ "`python -c "import gdal; print(gdal.VersionInfo())"`" == "2020200" ]
[ "`python -c "import numpy; print(numpy.__version__)"`" == "1.14.0" ]
[ "`python -c "import scipy; print(scipy.__version__)"`" == "1.0.0" ]
[ "`python -c "import sklearn; print(sklearn.__version__)"`" == "0.19.1" ]
[ "`python -c "import jobtastic; print(jobtastic.__version__)"`" == "2.0.0" ]
[ "`python -c "import tensorflow; print(tensorflow.__version__)"`" == "1.5.0" ]
[ "`python -c "import keras; print(keras.__version__)"`" == "2.1.3" ]
[ "`python -c "import pycodestyle; print(pycodestyle.__version__)"`" == "2.3.1" ]
[ "`python -c "import requests; print(requests.__version__)"`" == "2.18.4" ]
[ "`python -c "import sphinx; print(sphinx.__version__)"`" == "1.6.7" ]
[ "`python -c "import channels; print(channels.__version__)"`" == "2.0.2" ]
[ "`pip3 show sphinx-js | grep '^Version:' | cut -d' ' -f 2`" == "2.3.1" ]
python -c "import unittest"

# test Rabbit MQ Server version
dpkg -s rabbitmq-server | grep -i version | cut -d' ' -f 2
[ "`dpkg -s rabbitmq-server | grep -i version | cut -d' ' -f 2`" == "3.5.7-1ubuntu0.16.04.2" ]

echo "All tests Succeeded!"
