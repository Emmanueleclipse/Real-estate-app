#!/bin/bash
# Set up Digital Ocean VPS, (c) BienFacile 2014

UBUNTU_PACKAGES="python-setuptools mysql-client mysql-server python-mysqldb python-imaging"
REMOVE_PACKAGES="postgresql"
PYTHON_PACKAGES="django django-user-sessions django-grappelli django-widget-tweaks pika boto slimit csscompressor"

INSTALL_PATH="/home/sites/django/bienfacile"
INSTALL_PROJECT="marchand"

MYSQL_PASSWORD="8aZIpS39I1zvv9uT"

echo "Removing not required packages: $REMOVE_PACKAGES"
apt-get --purge remove $REMOVE_PACKAGES

echo 'Installing mysql'
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $MYSQL_PASSWORD"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $MYSQL_PASSWORD"
sudo apt-get -y install mysql-server
MYSQL=`which mysql`
$MYSQL --user=root --password=$INSTALL_PROJECT -e "CREATE DATABASE IF NOT EXISTS bf_developer; GRANT ALL ON bf_developer.* TO 'bf_developer'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD'; FLUSH PRIVILEGES;"
$MYSQL --user=root --password=$INSTALL_PROJECT bf_classified < $INSTALL_PATH/$INSTALL_PROJECT/sql/bf_developer-latest.sql

echo "Installing new packages: $UBUNTU_PACKAGES"
apt-get install $UBUNTU_PACKAGES

echo "Installing python modules: $PYTHON_PACKAGES"
easy_install $PYTHON_PACKAGES

echo 'Setting up web server'
sed -i -e 's|/home/django/django_project/django_project|'$INSTALL_PATH'/'$INSTALL_PROJECT'|g' /etc/nginx/sites-enabled/django
sed -i -e 's|/home/django|'$INSTALL_PATH/$INSTALL_PROJECT'|g' /etc/init/gunicorn.conf
sed -i -e 's|django_project|'$INSTALL_PROJECT'|g' /etc/init/gunicorn.conf
service nginx restart
service gunicorn restart
echo "Done."