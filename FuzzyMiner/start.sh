#!/bin/sh
uwsgi --ini /var/www/html/FuzzyMiner/uwsgi.ini
uwsgi --pidfile /var/www/html/FuzzyMiner/uwsgi.pid \
      --http 10.172.17.3:8000 \
      --uid root \
      --gid root \
      --vacuum \
      --chdir /var/www/html/FuzzyMiner \
      --wsgi-file FuzzyMiner/wsgi.py \
      --module FuzzyMiner.wsgi:miner \
      --cheaper-algo spare \
      --cheaper 2 \
      --cheaper-initial 3 \
      --workers 10 \
      --cheaper-step \
      --enable-threads \
      --threads 5 \
      --idle 360 \
      --post-buffering 8192 \
      --no-threads-wait
