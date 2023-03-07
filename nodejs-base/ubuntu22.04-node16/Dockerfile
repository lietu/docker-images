FROM lietu/ubuntu-base:22.04

ENV \
    GID=1000 \
    GROUP="api" \
    UID=1000 \
    USER="api" \
    ENV_LAST_LINE="LEAVE-ME-HERE"

# Run docker/base-prepare.sh
WORKDIR /src/
COPY docker /src/docker
RUN : \
 && set -exu \
 && bash /src/docker/base-prepare.sh \
 && rm -rf /src/docker \
 && :
