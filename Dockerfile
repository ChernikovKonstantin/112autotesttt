FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
apt upgrade -y && \
apt install -y dialog apt-utils language-pack-ru

ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales

RUN set -xe
RUN apt install -y --no-install-recommends python3-pip curl jq default-jre
RUN apt update && apt install -y gcc python3.8-dev


RUN apt install -y tzdata && \
ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

RUN pip3 install psycopg2-binary

WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt