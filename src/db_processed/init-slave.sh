#!/bin/bash
set -e

REP_USER=$(cat /tmp/postgresql/replication.txt | awk '{print $1}')
REP_PASS=$(cat /tmp/postgresql/replication.txt | awk '{print $2}')
DB_NAME=$(cat /tmp/postgresql/database.txt | awk '{print $1}')
DB_USER=$(cat /tmp/postgresql/database.txt | awk '{print $2}')

echo "Cleaning up old cluster directory"
rm -rf ${PGDATA}/*

echo "Starting base backup as replicator"
pg_basebackup -h ${MASTER_PORT_5432_TCP_ADDR} -D ${PGDATA} -U ${REP_USER} -vP

echo "Creating pg_hba.conf..."
sed -e "s/\${REP_USER}/$REP_USER/" \
    -e "s/\${DB_NAME}/$DB_NAME/" \
    -e "s/\${DB_USER}/$DB_USER/" \
    /tmp/postgresql/pg_hba.conf \
    > $PGDATA/pg_hba.conf
echo "Creating pg_hba.conf complete."

echo "Creating postgresql.conf..."
cp /tmp/postgresql/postgresql.conf $PGDATA/postgresql.conf
echo "hot_standby = on" >> $PGDATA/postgresql.conf

echo "Writing recovery.conf file"
cat > ${PGDATA}/recovery.conf <<EOS
standby_mode = 'on'
primary_conninfo = 'host=${MASTER_PORT_5432_TCP_ADDR} port=5432 user=${REP_USER} password=${REP_PASS}'
trigger_file = '/tmp/postgresql.trigger'
EOS

mkdir /var/lib/postgresql/archive
chown postgres:postgres /var/lib/postgresql/archive
chown -R postgres:postgres ${PGDATA}