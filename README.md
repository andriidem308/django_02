# Hillel project django_02

## Run gunicorn

```bash
make gunicorn_run
```

## Collect static files
```bash
make collect_static
```

## uWSGI & NGiNX start
### Step 1: Install NGINX
```bash
sudo apt install nginx
```
### Configure nginx.conf file
```bash
$ cd /etc/nginx/
$ nano nginx.conf
```

Delete all from file, then paste this code:
<br>***Notice:*** use needed directory, mine used here like example
```bash
events{}

http {
    include /etc/nginx/mime.types;
    sendfile on;
    server {
        listen 80;
        listen [::]:80;
        
        server_name 127.0.0.1 ssb.com;
        location /static/ {
          root /home/godfather/Documents/programming/django_02/static_content ;
        }
        
        location / {
          proxy_pass http://127.0.0.1:8081;
        }
    }
}
```

### Step 3: Start, Restart, Stop NGINX
*Start*
```bash
$ systemctl start nginx 
```
*Restart*
```bash
$ systemctl restart nginx 
```
*Stop*
```bash
$ systemctl stop nginx 
```