FROM lietu/nginx-base:latest

ADD site.conf /etc/nginx/conf.d
ADD 40-generate-keys.sh /docker-entrypoint.d

RUN set -exu \
 && apk add openssl
