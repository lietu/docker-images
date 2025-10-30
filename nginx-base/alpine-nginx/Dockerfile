FROM nginx:stable-alpine

ENV PARSE_TEMPLATE_VERSION=v1.0.2 \
    PARSE_TEMPLATE_HASH_AMD64=518e467ee3329815125f25c364ae899b1078d329e326d3cc7d2825ba2acdc9f2 \
    PARSE_TEMPLATE_HASH_ARM64=1c197e8a71397f65e97d99f7dd025c08839a48b50995f4f5b13600ae0de4221e \
    KEEP_THIS_LAST_LINE=""

RUN set -exu \
 && apk update \
 && apk upgrade --available \
 && apk add --virtual build-deps curl \
 && if [[ $(uname -m) == "x86_64" ]]; then \
      curl -L -o /usr/bin/parse-template https://github.com/cocreators-ee/parse-template/releases/download/${PARSE_TEMPLATE_VERSION}/parse-template_Linux_x86_64; \
      echo "${PARSE_TEMPLATE_HASH_AMD64}  /usr/bin/parse-template" | sha256sum -c; \
    else \
      curl -L -o /usr/bin/parse-template https://github.com/cocreators-ee/parse-template/releases/download/${PARSE_TEMPLATE_VERSION}/parse-template_Linux_arm64; \
      echo "${PARSE_TEMPLATE_HASH_ARM64}  /usr/bin/parse-template" | sha256sum -c; \
    fi \
 && chmod +x /usr/bin/parse-template \
 && mkdir -p /run/nginx/ \
 && apk del build-deps \
 && rm /etc/nginx/conf.d/default.conf \
 && rm -rf /var/cache/apk \
 && :

ADD nginx.conf /etc/nginx/
