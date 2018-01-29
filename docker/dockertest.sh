error() {
   echo "ERROR in DOCKER UNIT TEST!!!!!!" 
   exit -1
  }
trap error ERR



python --version
python -c "print('Hello World')"

