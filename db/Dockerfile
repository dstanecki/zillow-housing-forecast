FROM mariadb:latest

COPY /data/data.csv /docker-entrypoint-initdb.d/

COPY /data/import-data.sql /docker-entrypoint-initdb.d/