FROM mariadb:latest

COPY ./data.csv /docker-entrypoint-initdb.d/

COPY ./import-data.sql /docker-entrypoint-initdb.d/
