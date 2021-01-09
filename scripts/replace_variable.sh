#!/bin/bash
user=`whoami`
ip=`hostname -I`
cudp=`dirname "$PWD"`
path=`dirname $cudp`

echo "Current user: $user"
echo "Local ip address: $ip"
echo "Your path to the project: $path"

cp -v ./nginx.conf{.example,}
cp -v ./uwsgi.ini{.example,}

sed -i 's/<USER>/'"$user"'/g' uwsgi.ini
sed -i 's/<USER>/'"$user"'/g' nginx.conf

sed -i 's/<YOUR_IP>/'"$ip"'/g' uwsgi.ini
sed -i 's/<YOUR_IP>/'"$ip"'/g' nginx.conf

sed -i 's#<YOUR_PATH>#'"$path"'#g' uwsgi.ini
sed -i 's#<YOUR_PATH>#'"$path"'#g' nginx.conf
