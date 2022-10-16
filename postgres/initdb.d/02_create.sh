#!/usr/bin/env bash
psql --dbname postgres --username "postgres" <<-EOSQL
CREATE USER ${TICKER_USER} WITH PASSWORD '${TICKER_USER_PASSWORD}';
CREATE DATABASE ${TICKER_DBNAME} WITH OWNER = ${TICKER_USER};  
EOSQL
