
apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install bleach
pip install github-flask
pip install dicttoxml
postgres -c 'createuser -dRS vagrant'
vagrant -c 'createdb'
#su vagrant -c 'createdb forum'
#su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'