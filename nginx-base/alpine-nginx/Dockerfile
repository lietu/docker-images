FROM nginx:stable-alpine

ENV PARSE_TEMPLATE_VERSION=v1.0.1 \
    PARSE_TEMPLATE_HASH=dcfbc9e843292664aab43cd942694019ae566dc6ab83567f4339e942da76360b

RUN set -exu \
 && apk update \
 && apk upgrade --available \
 && apk add --virtual build-deps curl \
 && curl -L -o /usr/bin/parse-template https://github.com/cocreators-ee/parse-template/releases/download/${PARSE_TEMPLATE_VERSION}/parse-template_Linux_x86_64 \
 && echo "${PARSE_TEMPLATE_HASH}  /usr/bin/parse-template" | sha256sum -c \
 && chmod +x /usr/bin/parse-template \
 && mkdir -p /run/nginx/ \
 && apk del build-deps \
 && rm /etc/nginx/conf.d/default.conf \
 && rm -rf /var/cache/apk \
 && :

ADD nginx.conf /etc/nginx/
