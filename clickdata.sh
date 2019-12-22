#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE oanda;
    CREATE TABLE oanda.daily_prices (x Int32) ENGINE = Log;
EOSQL

clickhouse client -n <<-EOSQL
    CREATE DATABASE oanda;
    CREATE TABLE oanda.monthly_prices (x Int32) ENGINE = Log;
EOSQL