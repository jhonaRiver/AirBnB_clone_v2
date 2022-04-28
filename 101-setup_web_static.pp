# Redo task 0 with Puppet

exec {'Nginx installation':
     command  => 'sudo apt-get update -y; sudo apt-get install nginx -y',
     provider => shell
}

exec {'Creating folders':
     command  => 'sudo mkdir -p /data/web_static/releases/test/;
                  sudo mkdir -p /data/web_static/shared/',
     provider => shell,
     require  => Exec['Nginx installation']
}

exec {'Fake HTML':
     command  => 'echo "Fake text" | sudo tee /data/web_static/releases/test/index.html',
     provider => shell,
     require  => Exec['Creating folders']
}

exec {'Creating SL':
     command  => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
     provider => shell,
     require  => Exec['Fake HTML']
}

exec {'Owner change':
     command  => 'chown -R ubuntu:ubuntu /data/',
     provider => shell,
     require  => Exec['Creating SL']
}

exec {'Config file':
     command  => 'sudo sed -i "42i\ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default',
     provider => shell,
     require  => Exec['Owner change']
}

exec {'Nginx restart':
     command  => 'sudo service nginx restart',
     provider => shell,
     require  => Exec['Location thing']
}
