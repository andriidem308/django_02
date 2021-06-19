# ------------- nginx-server

ssh root@143.198.65.32
# 10.124.0.2


cat ~/.ssh/authorized_keys -- тут уже будет мой публичный ключ

apt update && apt upgrade

apt install nginx

systemctl status nginx



open in chrome: 143.198.65.32



mkdir -p /var/html/bread_blog_celery/static_content

vim /etc/nginx/sites-available/default

upstream django {
	server 10.124.0.4:8081;
}
server {
	listen 80;
	listen [::]:80;
	server_name _;

	location = /favicon.ico { access_log off; log_not_found off; }

	location /static/ {
		root /var/html/bread_blog_celery/static_content;
	}

	location / {
		proxy_pass http://django;
	}
}



systemctl enable --now nginx
systemctl restart nginx




# ------------- back-server
ssh root@143.198.106.128
# 10.124.0.4

apt update && apt upgrade

apt install python3-virtualenv

mkdir -p /var/www/bread_blog_celery
adduser ubuntu
chown -R ubuntu:ubuntu /var/www/bread_blog_celery*
su - ubuntu

cd /var/www/bread_blog_celery
git clone https://github.com/romanitalian/bread_blog_celery
cd bread_blog_celery

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

make run
make gunicorn

which gunicorn
/var/www/bread_blog_celery/bread_blog_celery/venv/bin/gunicorn




CTRL+D


# https://docs.gunicorn.org/en/stable/deploy.html
vim /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
# Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
# the specific user that our service will run as
User=ubuntu
Group=ubuntu
# another option for an even more restricted service is
# DynamicUser=yes
# see http://0pointer.net/blog/dynamic-users-with-systemd.html
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/bread_blog_celery/bread_blog_celery
ExecStart=/var/www/bread_blog_celery/bread_blog_celery/venv/bin/gunicorn -w 1 -b 0.0.0.0:8081 --chdir /var/www/bread_blog_celery/bread_blog_celery/src core.wsgi --timeout 60 --log-level debug --max-requests 10000
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=15
# PrivateTmp=true

[Install]
WantedBy=multi-user.target



systemctl enable --now gunicorn
# systemctl restart gunicorn
systemctl status gunicorn

sudo journalctl -f -u gunicorn


open in chrome: 143.198.106.128


su - ubuntu
ssh-keygen
cat ~/.ssh/id_rsa.pub

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3zeNX4akFEKfYLyz0DxGBlni4gyschRxjPP/MNIbfFBZl99iB7AMGCGs3czjkfRcCCwfQ/ed5/BxBShXMO7BXXrvUVC9jtxg0lZQkZr+/xw7rHWUzFr5dML/nplUq2WTZgs1PUlI0jWJdD/fygL1+r8+HWAIevTuzdXWE+SfF0mOgZzuVnuYK5lFhc8BKOLaKszZMrM9oInqpKK8Tv6F2qwHSSAEtjxJ9hlfzEPDVZZBGvoDTagYrkN1EoVYsvmJanG+pvex+7odcRbz31UDlVhVnbPbwb+XlBlSehKANAIhu166OWOcfgguz2wcrjP+syFsGKssPhLTp/6NZcMt3Nnjwxb/UPWv032KhjFn+31V5/D5v+5VWX0M16uo5AgBDDjo4IYMs8cmIRPilAFcOuq1CYlYQzQQbsCR2Lz30sIXMKaZ65suTwGEAzuU6TuR39vSDicMoXOGhqAXbeh8ZR/oMIkvD6EJL3oqpJWjvMfRllWdSYOehVUg5RCl+6bc= ubuntu@back-server


# ON MAC
ssh root@143.198.65.32
vim ~/.ssh/authorized_keys

# ON back-server
ssh root@10.124.0.2

cd /var/www/bread_blog_celery/bread_blog_celery
scp -r static_content/* root@10.124.0.2:/var/html/bread_blog_celery/static_content







# ------------- DB-server
ssh root@143.198.106.125
# 10.124.0.3

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04-ru

apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
sudo su - postgres
psql


drop database bread3;

CREATE DATABASE bread3;
CREATE USER bread WITH PASSWORD 'bread';

ALTER ROLE bread SET client_encoding TO 'utf8';
ALTER ROLE bread SET default_transaction_isolation TO 'read committed';
ALTER ROLE bread SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE bread3 TO bread;

\c bread

\q



psql -U postgres -c 'SHOW config_file'

vim /etc/postgresql/12/main/postgresql.conf
# listen_addresses = '*'

vim /etc/postgresql/12/main/pg_hba.conf
# host 	all	all	0.0.0.0/*		md5

service postgresql restart
service postgresql status

# ON back-server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bread',
        'USER': 'bread',
        'PASSWORD': 'bread',
        'HOST': '10.124.0.3',
        'PORT': '',
    }
}


make run

cd src
python manage.py makemigrations main
python manage.py makemigrations account




pip install django
pip install celery
pip install faker
pip install flake8
pip install gunicorn
pip install django-extensions
pip install django-debug-toolbar
pip install psycopg2-binary



# -------- memcached
apt install memcached

# --------- rabbitmq

sudo apt-get install curl gnupg debian-keyring debian-archive-keyring apt-transport-https -y

sudo apt-key adv --keyserver "hkps://keys.openpgp.org" --recv-keys "0x0A9AF2115F4687BD29803A206B73A36E6026DFCA"
sudo apt-key adv --keyserver "keyserver.ubuntu.com" --recv-keys "F77F1EDA57EBB1CC"
curl -1sLf 'https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey' | sudo apt-key add -

sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
deb http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu bionic main
deb-src http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu bionic main

deb https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ bionic main
deb-src https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ bionic main
EOF

sudo apt-get update -y

sudo apt-get install -y erlang-base \
    erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
    erlang-runtime-tools erlang-snmp erlang-ssl \
    erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

sudo apt-get install rabbitmq-server -y --fix-missing

