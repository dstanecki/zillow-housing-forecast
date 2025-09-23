FROM mariadb:latest

# Install mysql client
RUN apt-get update && apt-get install -y mariadb-client && rm -rf /var/lib/apt/lists/*

COPY ./healthcheck.sh /usr/local/bin/healthcheck.sh

RUN chmod +x /usr/local/bin/healthcheck.sh

COPY ./data.csv /docker-entrypoint-initdb.d/

COPY ./zip_centroids.csv /docker-entrypoint-initdb.d/

COPY ./import-data.sql /docker-entrypoint-initdb.d/
