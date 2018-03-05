#!/bin/bash

if [ "$1" == "local" ]; then
  server="localhost"
else
  server="www.citynet.online citynet.online"
fi
echo "Configuring with server=$server"

cat > /etc/nginx/sites-enabled/default <<EOF
server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;

    ssl_dhparam  /etc/nginx/ssl/dhparam.pem;
    server_name $server ;
    charset utf-8;
    client_max_body_size 100M;   # adjust to taste
    ssl on;
    ssl_certificate      /etc/nginx/ssl/certs/myssl.crt;
    ssl_certificate_key  /etc/nginx/ssl/private/myssl.key;

    location /ws/ {
        proxy_pass http://127.0.0.1:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade websocket;
        proxy_set_header Connection upgrade;
      }
    location /static/ {
        autoindex on;
        root   /var/www/;
     }
    location / {
       	    proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;

            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_redirect     off;
            proxy_set_header   Host \$host;
            proxy_set_header   X-Real-IP \$remote_addr;
            proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host \$server_name;
        }
}
server {
  listen         80;
  listen    [::]:80;
  server_name    $server ;
  return         301 https://\$server_name\$request_uri;
}
EOF

mkdir -p /etc/nginx/ssl
mkdir -p /var/log/nginx
# generate new key:
openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048

openssl req  -nodes -new -x509  -keyout myssl.key -out myssl.crt \
  -subj "/C=DE/ST=NRW/L=Berlin/O=My Inc/OU=DevOps/CN=www.example.com/emailAddress=dev@www.example.com"



echo "Copying certificate (myssl.crt) to /etc/nginx/ssl/certs/"
mkdir -p  /etc/nginx/ssl/certs
mv myssl.crt /etc/nginx/ssl/certs/

echo "Copying key (myssl.key) to /etc/nginx/ssl/private/"
mkdir -p  /etc/nginx/ssl/private
mv myssl.key /etc/nginx/ssl/private/

nginx -t
