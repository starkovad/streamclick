#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    create database oanda;

    create table oanda.inst_info (inst String, type String) ENGINE = Log;

    create table oanda.currency_M2 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_M3 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_M4 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_M5 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_M10 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_M15 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_M30 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.currency_H1 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    
    create table oanda.metal_M2 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_M3 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_M4 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_M5 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_M10 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_M15 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_M30 (datetime DateTime, inst String, price Float32) ENGINE = Log;
    create table oanda.metal_H1 (datetime DateTime, inst String, price Float32) ENGINE = Log;
EOSQL