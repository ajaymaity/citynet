sudo docker pull asegroup11/all_servers:citynet
sudo docker run --hostname "cityback_beat" \
  -v "/home/ubuntu/config_private_citynet/":/app/config_private/ \
  -v /home/ubuntu/citynet:/app \
  -d --restart unless-stopped \
  asegroup11/all_servers:citynet \
  /app/prod/start_prod_beat.sh
