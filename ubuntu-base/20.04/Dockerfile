FROM ubuntu:20.04

ENV \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ="UTC" \
    ENV_LAST_LINE="LEAVE-ME-HERE"

RUN : \
 && apt-get update \
 && apt-get upgrade -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /root/.cache \
 && rm -rf /usr/share/doc \
 && :
