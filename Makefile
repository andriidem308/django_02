MANAGE = python3 manage.py
PROJECT_DIR = $(shell pwd)
WSGI_PORT=8081

run:
	$(MANAGE) runserver 0.0.0.0:8000

make-migration:
	$(MANAGE)  makemigrations

migrate:
	$(MANAGE) migrate

lint:
	flake8 .

gunicorn_run:
	gunicorn -w 4 -b 0.0.0.0:$(WSGI_PORT) --chdir $(PROJECT_DIR) django_02.wsgi --timeout 60 --log-level debug --max-requests 10000

collect-static:
	$(MANAGE) collectstatic

run_nginx:
	systemctl start nginx

stop_nginx:
	systemctl stop nginx

reload_nginx:
	systemctl reload nginx

unittest:
	pytest

test:
	pytest --cov=main --cov-report=html --cov-fail-under=40