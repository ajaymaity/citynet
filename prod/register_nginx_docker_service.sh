docker volume inspect letsencrypt &>/dev/null || docker volume create letsencrypt
sudo docker run --hostname "cityback_nginx" \
  -p 443:443 -p 80:80 \
  -v nginx_conf:/etc/nginx/ \
  -v "/home/ubuntu/config_private_citynet/":/app/config_private/ \
  -v /home/ubuntu/citynet:/app \
  -v letsencrypt:/etc/letsencrypt/ \
  -d --restart unless-stopped \
  asegroup11/all_servers:citynet \
  /app/prod/start_prod_nginx.sh
