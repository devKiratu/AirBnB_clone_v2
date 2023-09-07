#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# update package repository
sudo apt update

# install nginx
sudo apt install nginx -y

# create required folders:
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
content="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$content" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# create symlink
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# change ownership for data folder
sudo chown -R ubuntu:ubuntu /data/

# update nginx configuration to server /web_static/current at /hbnb_static
config="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n"
sudo sed -i "/server_name _;/a\\$config" /etc/nginx/sites-enabled/default

# restart nginx
sudo service nginx restart
