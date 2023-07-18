#!/usr/bin/env bash
# Script sets up web servers for deployment of web_static.

# dpkg -s nginx &> /dev/null

if [ "$(dpkg -s nginx &> /dev/null)" -ne 0 ] ; then
	sudo apt update
	sudo apt install nginx -y
fi

if  [ ! -d /data ]; then
	sudo mkdir /data
fi

if [ ! -d /data/web_static ] ; then
	sudo mkdir /data/web_static
fi

if [ ! -d /data/web_static/releases ] ; then
	sudo mkdir /data/web_static/releases
fi

if [ ! -d /data/web_static/shared ] ; then
	sudo mkdir /data/web_static/shared
fi

if [ ! -d /data/web_static/releases/test ] ; then
	sudo mkdir /data/web_static/releases/test/
fi

sudo echo "Hello World!!" > /data/web_static/releases/test/index.html

if [ ! -L /data/web_static/current ] ; then
	sudo ln -s /data/web_static/releases/test/ /data/web_static/current
else
	rm /data/web_static/current
	sudo ln -s /data/web_static/releases/test/ /data/web_static/current
fi

sudo chown -R ubuntu:ubuntu /data

sudo sed -i "s|server_name _;|server_name zihco.tech;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}|" /etc/nginx/sites-available/default

sudo sed -i "s|root /var/www/html;|root /data/web_static/;|" /etc/nginx/sites-available/default

sudo service nginx restart
