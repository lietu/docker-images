ARG LOCAL_REGISTRY=""
FROM ${LOCAL_REGISTRY}ubuntu-base:24.04

ENV \
    GID=1001 \
    GROUP="api" \
    UID=1001 \
    USER="api" \
    ENV_LAST_LINE="LEAVE-ME-HERE"

# Run docker/base-prepare.sh
WORKDIR /src/
COPY docker /src/docker
RUN : \
 && set -exu \
 && bash /src/docker/base_prepare.sh \
 && rm -rf /src/docker \
 && :
