FROM python:3.7

MAINTAINER Eric eric.pireirik@gmail.com

ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/html/FuzzyMiner

ADD . /var/www/html/FuzzyMiner

RUN mkdir -p /var/www/html/FuzzyMiner \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && cd /var/www/html/FuzzyMiner \
    && chmod +x ./preparation.sh \
    && ./preparation.sh \
    && chmod +x ./start.sh

ENTRYPOINT /var/www/html/FuzzyMiner/start.sh

EXPOSE 8000
