#!/bin/sh
uwsgi --ini /var/www/html/FuzzyMiner/uwsgi.ini
# uwsgi --http 10.172.17.3:8000 --uid root --gid root --chdir /var/www/html/FuzzyMiner --wsgi-file FuzzyMiner/wsgi.py --module FuzzyMiner.wsgi:miner
