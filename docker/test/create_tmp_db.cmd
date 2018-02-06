# modify db port to 5439 and run postgresql
sed -i 's/^\(port =\).*/\1 5439/' /etc/postgresql/9.5/main/postgresql.conf
/etc/init.d/postgresql start

sleep 2
# create tmpdb
su postgres <<EOF
psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker &&\
    PGPASSWORD=docker psql -h localhost -p 5439 -U docker -c 'CREATE EXTENSION postgis;'
EOF
