release: python manage.py migrate
web: gunicorn payments_project.wsgi --log-file -
worker: celery -A payments_project worker -E -B --loglevel=DEBUG
