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
  apt-get install -y software-properties-common

RUN echo $TZ > /etc/timezone && \
    apt-get install -y tzdata curl && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata 


# Install packages, Java and nodejs.
RUN \
  add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable &&\
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  curl -sL https://deb.nodesource.com/setup_8.x | bash - &&\
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y build-essential oracle-java8-installer \
                     curl git htop man vim wget python3-pip postgresql \
                     gdal-bin python3-gdal nodejs &&\
  rm -rf /var/lib/apt/lists/* &&\
  apt-get autoremove &&\
  apt-get clean &&\
  rm -rf /var/cache/oracle-jdk8-installer &&\
  rm -rf /var/lib/apt/lists/*

RUN \
    npm install -g mapbox-gl eslint


# Fix python default to 3
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
ADD requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt


# Add files.
ADD dockertest.sh /root/dockertest.sh

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

# Define default command.
CMD ["bash"]
