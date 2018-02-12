celery -A tasks worker --loglevel=info & $PID=&!
sleep 1.5

python testdataprocessing.py
$ret=$?

