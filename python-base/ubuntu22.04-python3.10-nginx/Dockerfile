FROM python-base:ubuntu22.04-python3.10

ENV \
    PARSE_TEMPLATE_HASH="8d1dc39e701b938f4874f3f8130cd3a324e7fa4697af36541918f9398dd61223" \
    PARSE_TEMPLATE_VERSION="v1.0.0" \
    ENV_LAST_LINE="LEAVE-ME-HERE"

# Run docker/base-prepare.sh
WORKDIR /src/
COPY docker /src/docker
RUN : \
 && set -exu \
 && bash /src/docker/base-prepare.sh \
 && rm -rf /src/docker \
 && :
