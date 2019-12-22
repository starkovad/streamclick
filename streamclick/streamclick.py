import streamlit as st
from clickhouse_driver import Client


clk = Client('click-server', port='9000')
ans = clk.execute('show databases')
