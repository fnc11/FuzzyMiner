#!/bin/bash
cd /var/www/html/FuzzyMiner
secret=`python3.7 ./secret.py`

# mv -v ./uwsgi.ini{.example,}
mv -v ./FuzzyMiner/settings.py{.example,}

sed -i 's/<YOUR_SECRET_KEY>/'"$secret"'/g' ./FuzzyMiner/settings.py
