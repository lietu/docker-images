#!/usr/bin/env sh

mkdir -p /etc/nginx/ssl

openssl req -x509 -nodes \
    -days 3650 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/ssl.key \
    -out /etc/nginx/ssl/ssl.crt \
    -subj "/C=/ST=/L=/O=/OU=/CN="
