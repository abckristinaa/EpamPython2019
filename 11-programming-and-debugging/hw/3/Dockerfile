FROM debian:stretch-slim

RUN apt-get update \
&& apt-get install make \
&& apt-get install openssl -y \
&& apt-get install zlib1g-dev -y \
&& apt-get install checkinstall -y \
&& apt-get install wget -y

RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
RUN tar xvf Python-3.6.0.tgz \
&& cd /Python-3.6.0 \
&& ./configure \
&& make altinstall

RUN python3.6 --version

COPY . ./abckristinaa/