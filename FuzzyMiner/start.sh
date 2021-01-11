#!/bin/sh
# uwsgi --ini /usr/share/nginx/FuzzyMiner/uwsgi.ini
uwsgi --pidfile /usr/share/nginx/FuzzyMiner/uwsgi.pid \
      --http 10.172.17.3:8000 \
      --uid root \
      --gid root \
      --vacuum \
      --chdir /usr/share/nginx/FuzzyMiner \
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
