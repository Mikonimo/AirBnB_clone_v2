# manifest.pp

# Ensure the system is up-to-date
exec { 'apt-get update':
  command => '/usr/bin/apt-get update',
  path    => ['/usr/bin', '/usr/sbin'],
}

# Ensure nginx is installed
package { 'nginx':
  ensure => installed,
  require => Exec['apt-get update'],
}

# Ensure the required directories exist
file { ['/data', '/data/web_static', '/data/web_static/shared', '/data/web_static/releases', '/data/web_static/releases/test']:
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => Package['nginx'],
}

# Create the index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  require => File['/data/web_static/releases/test'],
}

# Create a symbolic link to the test release
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test/index.html'],
}

# Ensure the ownership of /data directory
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  recurse => true,
  require => File['/data/web_static/releases/test/index.html'],
}

# Configure nginx
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
}

# Template for nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => template('nginx/default.erb'),
  require => Package['nginx'],
}

# Ensure nginx service is running and enabled
service { 'nginx':
  ensure     => running,
  enable     => true,
  subscribe  => File['/etc/nginx/sites-available/default'],
}

# Template file for nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => epp('nginx/default.epp'),
}

# EPP template for nginx configuration
epp('nginx/default.epp', '<%- | String $server_name = "_", String $alias = "/data/web_static/current/" | -%>
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name <%= $server_name %>;

    location / {
        try_files $uri $uri/ =404;
    }

    location /hbnb_static/ {
        alias <%= $alias %>;
    }
}
')
