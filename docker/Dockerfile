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
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  curl -sL https://deb.nodesource.com/setup_8.x | bash - &&\
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y --no-install-recommends build-essential oracle-java8-installer \
                     curl git htop man vim wget python3-pip postgresql postgis\
                      postgresql-9.5-postgis-scripts postgresql-9.5-postgis-2.4 \
                     gdal-bin python3-gdal nodejs python3-psutil &&\
  rm -rf /var/lib/apt/lists/* &&\
  apt-get autoremove &&\
  apt-get clean &&\
  rm -rf /var/cache/oracle-jdk8-installer &&\
  rm -rf /var/lib/apt/lists/*


# Fix python default to 3
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
ADD requirements.txt /root/requirements.txt
RUN pip3 install setuptools &&\
    pip3 install --no-cache-dir -r /root/requirements.txt

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
#Configure postgres db
USER postgres

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add files.
ADD dockertest.sh /root/dockertest.sh

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

USER root
# Define default command.
CMD ["bash"]
