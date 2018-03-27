sudo docker run --hostname "cityback_daphne" -p 8000:8000 \
  -v "/home/ubuntu/config_private_citynet/":/app/config_private/ \
  -v /home/ubuntu/citynet:/app -d --restart unless-stopped \
  asegroup11/all_servers:citynet /app/prod/start_prod_no_beat.sh
