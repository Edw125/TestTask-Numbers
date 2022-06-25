/usr/bin/python manage.py runsslserver 127.0.0.1:9000
/usr/bin/celery -A TestTask worker -l INFO
