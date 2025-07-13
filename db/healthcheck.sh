#!/bin/sh

mariadb -h127.0.0.1 -uroot -p"$MYSQL_ROOT_PASSWORD" -D "$MYSQL_DATABASE" \
  -e "SELECT COUNT(*) FROM forecast;" | grep -q '[1-9]'
