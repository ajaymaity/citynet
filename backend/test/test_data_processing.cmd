celery -A tasks worker --loglevel=info & $PID=&!
sleep 1.5

python ../cityback/data_processing.py
$ret=$?
