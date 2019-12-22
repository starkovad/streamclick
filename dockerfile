FROM yandex/clickhouse-client

FROM python:latest
WORKDIR /streamclick
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .