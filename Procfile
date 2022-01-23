release: python src/manage.py migrate
web: gunicorn --pythonpath=src core.wsgi --workers 3 --log-file -
