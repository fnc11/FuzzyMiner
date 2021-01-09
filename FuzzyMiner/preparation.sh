#!/bin/bash
user=`whoami`
ip=`hostname -I | sed 's/[ \t]*$//g'`
cudp=`dirname "$PWD"`
path=`dirname $cudp`
secret=`python ./secret.py`

echo "Current user: $user"
echo "Local ip address: $ip"
echo "Your path to the project: $path"
echo "Your secret for settings.py: $secret"

cp -v ./uwsgi.ini{.example,}
cp -v FuzzyMiner/settings.py{.example,}

sed -i 's/<USER>/'"$user"'/g' uwsgi.ini
sed -i 's/<YOUR_IP>/'"$ip"'/g' uwsgi.ini
sed -i 's#<YOUR_PATH>#'"$path"'#g' uwsgi.ini

sed -i 's/<YOUR_IP>/'"$ip"'/g' FuzzyMiner/settings.py
sed -i 's/<YOUR_SECRET_KEY>/'"$secret"'/g' FuzzyMiner/settings.py
