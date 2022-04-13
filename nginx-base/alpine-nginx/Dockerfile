FROM nginx:stable-alpine

ENV PARSE_TEMPLATE_VERSION=v1.0.0 \
    PARSE_TEMPLATE_HASH=8d1dc39e701b938f4874f3f8130cd3a324e7fa4697af36541918f9398dd61223

RUN set -exu \
 && apk update \
 && apk upgrade --available \
 && apk add --virtual build-deps curl \
 && curl -L -o /usr/bin/parse-template https://github.com/cocreators-ee/parse-template/releases/download/${PARSE_TEMPLATE_VERSION}/parse-template-linux-amd64 \
 && echo "${PARSE_TEMPLATE_HASH}  /usr/bin/parse-template" | sha256sum -c \
 && chmod +x /usr/bin/parse-template \
 && mkdir -p /run/nginx/ \
 && apk del build-deps \
 && rm /etc/nginx/conf.d/default.conf \
 && rm -rf /var/cache/apk \
 && :

ADD nginx.conf /etc/nginx/
