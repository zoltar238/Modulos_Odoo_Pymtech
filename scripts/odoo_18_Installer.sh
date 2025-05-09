#!/bin/bash

#Creamos el usuario y grupo de sistema 'odoo':

sudo adduser --system --quiet --shell=/bin/bash --home=/opt/odoo --gecos 'odoo' --group odoo

#Creamos en directorio en donde se almacenará el archivo de configuración y log de odoo:

sudo mkdir /etc/odoo && sudo mkdir /var/log/odoo/

# Instalamos Postgres y librerías base del sistema:

sudo apt update

udo apt-get install -y python3-pip

sudo apt-get install -y python3-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev

sudo apt-get install -y git

sudo apt-get install -y npm

sudo npm install -g less less-plugin-clean-css

sudo apt-get install -y node-less

#Instalamos Postgres

sudo apt-get install -y postgresql

#Descargamos odoo version 18 desde git:

sudo git clone --depth 1 --branch 18.0 https://github.com/odoo/odoo /opt/odoo/odoo

#Damos permiso al directorio que contiene los archivos de OdooERP  e instalamos las dependencias de python3:

sudo chown odoo:odoo /opt/odoo/ -R && sudo chown odoo:odoo /var/log/odoo/ -R

cd /opt/odoo/odoo

sudo ./setup/debinstall.sh

#Descargamos dependencias e instalar wkhtmltopdf para generar PDF en odoo

sudo apt install fontconfig xfonts-base xfonts-75dpi -y

cd /tmp

wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb && sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb

sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin/ && sudo ln -s /usr/local/bin/wkhtmltoimage /usr/bin/

#Creamos un usuario 'odoo' para la base de datos:

sudo su - postgres -c "createuser -s odoo"

#Creamos la configuracion de Odoo:

sudo su - odoo -c "/opt/odoo/odoo/odoo-bin --addons-path=/opt/odoo/odoo/addons -s --stop-after-init"

#Creamos el archivo de configuracion de odoo:

sudo mv /opt/odoo/.odoorc /etc/odoo/odoo.conf

#Agregamos los siguientes parámetros al archivo de configuración de odoo:

sudo sed -i "s,^\(logfile = \).*,\1"/var/log/odoo/odoo-server.log"," /etc/odoo/odoo.conf

#Creamos el archivo de inicio del servicio de Odoo:

sudo cp /opt/odoo/odoo/debian/init /etc/init.d/odoo && sudo chmod +x /etc/init.d/odoo

sudo ln -s /opt/odoo/odoo/odoo-bin /usr/bin/odoo

sudo update-rc.d -f odoo start 20 2 3 4 5 .

sudo service odoo start