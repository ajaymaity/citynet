realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

path="$(dirname $(realpath $0))"

sudo docker pull redis:alpine

source ../../config_private_citynet/bash_import_secret_aws

sudo docker run --name some-redis -p 6379:6379 \
  -v nginx_conf:/etc/nginx/ \
  -v "${path}/../../config_private_citynet/redis-password":/run/secrets/redis-password
  -d --restart unless-stopped \
    redis:alpine --requirepass $$(cat /run/secrets/redis-password)
