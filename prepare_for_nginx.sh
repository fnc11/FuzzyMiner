#!/bin/bash
user=`whoami`
ip=`hostname -I`
path=`dirname $PWD`

echo "Current user: $user"
echo "Local ip address: $ip"
echo "Your path to the project: $path"

cp -v ./nginx.conf{.example,}

sed -i 's/<USER>/'"$user"'/g' nginx.conf
sed -i 's/<YOUR_IP>/'"$ip"'/g' nginx.conf
sed -i 's#<YOUR_PATH>#'"$path"'#g' nginx.conf
