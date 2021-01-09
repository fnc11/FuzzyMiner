FROM python:3.7

MAINTAINER Eric eric.pireirik@gmail.com

ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/html/FuzzyMiner

ADD . /var/www/html/FuzzyMiner

RUN mkdir -p /var/www/html/FuzzyMiner
    && /usr/local/bin/python -m pip install --upgrade pip
    && pip install -r requirements.txt
    && uwsgi --ini /var/www/html/FuzzyMiner/uwsgi.ini

EXPOSE 8000
