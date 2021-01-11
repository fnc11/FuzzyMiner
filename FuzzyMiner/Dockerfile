FROM ubuntu:16.04

MAINTAINER Eric eric.pireirik@gmail.com

ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/html/FuzzyMiner

ADD . /var/www/html/FuzzyMiner

RUN apt update -y \
    && apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev zlib1g-dev libc6-dev libbz2-dev libffi-dev libsqlite3-dev tk-dev libgdbm-dev python3-dev python3-setuptools wget \
    && cd /root && wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tar.xz \
    && tar -xvf Python-3.7.9.tar.xz \
    && cd /root/Python-3.7.9 \
    && ./configure \
    && make && make install \
    && mkdir -p /var/www/html/FuzzyMiner \
    && cd /var/www/html/FuzzyMiner \ && rm -rf /root/Python-3.7.9 \
    && pip3.7 install --upgrade pip \
    && pip3.7 install -r requirements.txt \
    && chmod +x ./preparation.sh \
    && ./preparation.sh \
    && chmod +x ./start.sh

ENTRYPOINT /var/www/html/FuzzyMiner/start.sh

EXPOSE 8000
