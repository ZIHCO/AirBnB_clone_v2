#!/usr/bin/env bash
# Script sets up web servers for deployment of web_static.

dpkg -s nginx &> /dev/null

if [ $? -ne 0 ] ; then
	sudo apt update
	sudo apt install nginx -y
fi

[ -d /data ]

if [ $? -ne 0 ] ; then
	sudo mkdir /data
fi

[ -d /data/web_static ]

if [ $? -ne 0 ] ; then
	sudo mkdir /data/web_static
fi

[ -d /data/web_static/releases ]

if [ $? -ne 0 ] ; then
	sudo mkdir /data/web_static/releases
fi

[ -d /data/web_static/shared ]

if [ $? -ne 0 ] ; then
	sudo mkdir /data/web_static/shared
fi

[ -d /data/web_static/releases/test/ ]

if [ $? -ne 0 ] ; then
	sudo mkdir /data/web_static/releases/test/
fi

sudo echo "Hello World!!" > /data/web_static/releases/test/index.html

[ -L /data/web_static/current ]

if [ $? -ne 0 ] ; then
	sudo ln -s /data/web_static/releases/test/ /data/web_static/current
else
	rm /data/web_static/current
	sudo ln -s /data/web_static/releases/test/ /data/web_static/current
fi
sudo chown -R ubuntu:ubuntu /data

sudo sed -i "s|server_name _;|server_name zihco.tech;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}|" /etc/nginx/sites-available/default

sudo sed -i "s|root /var/www/html;|root /data/web_static/;|" /etc/nginx/sites-available/default

sudo service nginx restart
