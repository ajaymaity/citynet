error() {
   echo "ERROR in DOCKER UNIT TEST!!!!!!" 
   exit -1
  }
trap error ERR



python --version 
[ `python3 --version | cut -d' ' -f2` == "3.5.2" ]
python -c "print('Hello World')"
java -version
