# This script sets up your web servers for the deployment of web_static by
#  setting up the necessary data folders and updating nginx configuration

# update package repository
exec { 'apt_update':
  command => '/usr/bin/apt update'
}

# install nginx
package { 'nginx':
  ensure  => installed,
  require => Exec['apt_update']
}

# create required directories
exec { 'create_directories':
  command => "/usr/bin/mkdir -p /data/ /data/web_static/ /data/web_static/releases/\
  /data/web_static/shared/ /data/web_static/releases/test/"
}

# create test file
$content="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => $content,
  require => Exec['create_directories']
}

# create a symlink to the test directory
exec { 'create_symlink':
  command => '/usr/bin/ln -s -f /data/web_static/releases/test/ /data/web_static/current',
  require => Exec['create_directories']
}

# change ownership for data folder
exec { 'change_data_ownership':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
  require => Exec['create_directories']
}

# update nginx configuration to server /web_static/current at /hbnb_static
$config="\\\n\tlocation /hbnb_static {\\n\t\talias /data/web_static/current;\\n\t}\\n"
exec { 'serve_hbnb_static':
  command => "/usr/bin/sed -i \"/server_name _;/a\\${config}\" /etc/nginx/sites-enabled/default",
  require => Package['nginx']
}

# restart nginx
exec { 'restart_nginx':
  command => '/usr/sbin/service nginx restart',
  require => Package['nginx']
}
