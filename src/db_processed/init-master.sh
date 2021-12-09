#!/bin/bash
set -e

REP_USER=$(cat /tmp/postgresql/replication.txt | awk '{print $1}')
REP_PASS=$(cat /tmp/postgresql/replication.txt | awk '{print $2}')
REP_PASS_MD5=$(echo -n "${REP_PASS}${REP_USER}" | md5sum | awk '{print $1}')
DB_NAME=$(cat /tmp/postgresql/database.txt | awk '{print $1}')
DB_USER=$(cat /tmp/postgresql/database.txt | awk '{print $2}')
DB_PASS=$(cat /tmp/postgresql/database.txt | awk '{print $3}')
DB_PASS_MD5=$(echo -n "${DB_PASS}${DB_USER}" | md5sum | awk '{print $1}')

echo "Creating pg_hba.conf..."
sed -e "s/\${REP_USER}/$REP_USER/" \
    -e "s/\${DB_NAME}/$DB_NAME/" \
    -e "s/\${DB_USER}/$DB_USER/" \
    /tmp/postgresql/pg_hba.conf \
    > $PGDATA/pg_hba.conf
echo "Creating pg_hba.conf complete."

echo "Creating postgresql.conf..."
cp /tmp/postgresql/postgresql.conf $PGDATA/postgresql.conf

echo "Creating replication user..."
# gosu postgres postgres --single <<-EOSQL
psql -c "CREATE ROLE ${REP_USER} PASSWORD 'md5${REP_PASS_MD5}' REPLICATION LOGIN;"
# EOSQL
echo "Creating replication user complete."

echo "Creating example database..."
# gosu postgres postgres --single <<-EOSQL
psql -c "CREATE DATABASE ${DB_NAME};"
psql -c "CREATE ROLE ${DB_USER} PASSWORD 'md5${DB_PASS_MD5}' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} to ${DB_USER};"
# EOSQL
echo "Creating example database complete."

mkdir /var/lib/postgresql/archive
chown postgres:postgres /var/lib/postgresql/archive
chown -R postgres:postgres ${PGDATA}