#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static
apt-get -y update
apt-get install -y nginx

# Creating relevant folders if they don't exists
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

config_f="/etc/nginx/sites-available/default"
config_b="\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

if ! grep -q  "location /hbnb_static/" "$config_f"; then
    sed -i "/server_name _;/ a $config_b" $config_f
fi
# Restart nginx
service nginx restart
exit 0
