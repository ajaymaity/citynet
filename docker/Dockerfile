#
# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu
#

# Pull base image.
FROM ubuntu:16.04

ENV TZ 'Europe/Dublin'
# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y --no-install-recommends software-properties-common &&\
  echo $TZ > /etc/timezone && \
  apt-get install -y tzdata curl && \
  rm /etc/localtime && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  dpkg-reconfigure -f noninteractive tzdata &&\
  rm -rf /var/lib/apt/lists/* &&\
  apt-get autoremove &&\
  apt-get clean &&\
  rm -rf /var/lib/apt/lists/*


# Install python, Java and nodejs.
RUN \
  add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable &&\
  curl -sL https://deb.nodesource.com/setup_8.x | bash - &&\
  apt-get update && \
  apt-get install -y --no-install-recommends build-essential rabbitmq-server redis-server\
                      curl git htop man vim wget python3-pip postgresql postgis\
                      postgresql-9.5-postgis-scripts postgresql-9.5-postgis-2.4 \
                      gdal-bin python3-gdal python3-dev nodejs python3-psutil tmux nginx \
                      libssl-dev &&\
  rm -rf /var/lib/apt/lists/* &&\
  apt-get autoremove &&\
  apt-get clean &&\
  rm -rf /var/lib/apt/lists/*

ADD .tmux.conf /root/.tmux.conf

# Fix python default to 3
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
ADD requirements.txt /root/requirements.txt
RUN pip3 install setuptools &&\
    pip3 install --no-cache-dir -r /root/requirements.txt

RUN locale-gen en_IE.UTF-8
ENV LANG en_IE.UTF-8
ENV LANGUAGE en_IE:en
ENV LC_ALL en_IE.UTF-8
#Configure postgres db

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
# RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
# RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

# add let's encrypt bot
RUN \
  add-apt-repository -y ppa:certbot/certbot &&\
  apt-get update && \
  apt-get install -y python3-certbot-nginx libcurl4-nss-dev &&\
  apt-get autoremove &&\
  apt-get clean &&\
  rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --compile --ignore-installed \
 --install-option="--with-nss" pycurl
# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log", "/var/lib/postgresql", "/etc/nginx"]

# ADD
RUN useradd -c 'Daphne user' -m -d /home/daphne -s /bin/bash daphne


# Expose the web ports
EXPOSE 80 443

# Set environment variables.
ENV HOME /root

# Define working directory.
RUN mkdir /app
WORKDIR /app

USER root
# Define default command.
CMD ["bash"]
