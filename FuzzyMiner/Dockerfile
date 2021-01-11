FROM centos:7

MAINTAINER Eric eric.pireirik@gmail.com

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/share/nginx/FuzzyMiner

ADD . /usr/share/nginx/FuzzyMiner

RUN yum update -y \
    && yum -y groupinstall "Development tools" \
    && yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel graphviz wget \
    && cd /root && wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tar.xz \
    && tar -xvf Python-3.7.9.tar.xz \
    && cd /root/Python-3.7.9 \
    && ./configure \
    && make && make install \
    && mkdir -p /usr/share/nginx/FuzzyMiner \
    && cd /usr/share/nginx/FuzzyMiner \ && rm -rf /root/Python-3.7.9 \
    && pip3.7 install --upgrade pip \
    && pip3.7 install -r requirements.txt \
    && chmod +x ./preparation.sh \
    && ./preparation.sh \
    && chmod +x ./start.sh

VOLUME ["/usr/share/nginx/FuzzyMiner/media"]

ENTRYPOINT /usr/share/nginx/FuzzyMiner/start.sh

EXPOSE 8000
