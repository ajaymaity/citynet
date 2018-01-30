error() {
   echo "ERROR in DOCKER UNIT TEST!!!!!!" 
   exit -1
  }
trap error ERR



python --version
[ `python3 --version | cut -d' ' -f2` == "3.5.2" ]
python -c "print('Hello World')"
[ `python -c "import django; print(django.__version__)"` == "1.11.6" ]
[ `python -c "import celery; print(celery.__version__)"` == "4.1.0" ]
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
#java -version
