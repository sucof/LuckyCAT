FROM phusion/baseimage:0.10.0
MAINTAINER Thomas Barabosch <thomas.barabosch@fkie.fraunhofer.de>

# install dependencies 
RUN apt-get update -y && apt-get install -y gcc cmake make wget screen gdb \
python automake git htop python3 build-essential python3-setuptools python3-dev \
python3-pip nginx
RUN pip3 install Flask flask-security flask-mongoengine bcrypt uwsgi

# copy f3c source into container and install
WORKDIR /opt
RUN mkdir /opt/luckycat && mkdir /opt/luckycat/samples && mkdir /opt/luckycat/results
COPY . /opt/luckycat
COPY docker/frontend/start_frontend.sh /opt/luckycat/

# create SSL certificate
RUN openssl req -subj '/CN=localhost' -x509 -newkey rsa:4096 -nodes -keyout /etc/nginx/conf.d/key.pem -out /etc/nginx/conf.d/cert.pem -days 365

EXPOSE 5000
CMD ["/bin/bash", "/opt/luckycat/start_frontend.sh"]
