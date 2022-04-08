FROM lietu/python-base:ubuntu20.04-python3.9

RUN --mount=type=cache,target=/var/lib/apt/lists/ \
    set -exu \
    # Devpi
 && pip install devpi-server devpi-web \
 && mkdir -p /cache \
 && devpi-init --serverdir /cache/.devpi/server \
    # apt-cacher-ng
 && apt-get update \
 && apt-get install -y apt-cacher-ng \
 && apt-get clean \
 && :

EXPOSE 3141
EXPOSE 3142

COPY entrypoint.sh ./
COPY apt-cacher-ng/* /etc/apt-cacher-ng/

ENTRYPOINT ["bash", "entrypoint.sh"]