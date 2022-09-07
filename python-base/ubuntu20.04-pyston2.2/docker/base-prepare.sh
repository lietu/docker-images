#!/usr/bin/env bash
#
# WARNING!
# ========
#
# THIS FILE IS NOT USED IN RUNTIME, ONLY WHILE BUILDING DOCKER IMAGES
# DO NOT ADD ANYTHING RUNTIME OR ENVIRONMENT SPECIFIC HERE
#
# This file is for installing the larger dependencies that rarely change such
# as OS packages, utilities and so on, for the build environment
#

# shellcheck disable=SC2039
set -exuo pipefail

bash /src/docker/scripts/create_user.sh

apt-get update

# build-essential will be essential with pyston
apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  build-essential \
  libffi-dev \
  libssl-dev \
  cargo \
  ""

bash /src/docker/scripts/install_pyston.sh
bash /src/docker/scripts/prepare_workon_dir.sh
bash /src/docker/scripts/install_poetry.sh

# Allow the next script to run as ${USER}
chown -R "${USER}":"${GROUP}" /src

bash /src/docker/scripts/configure_poetry.sh

# Cleanup
apt-get purge -y \
  cargo \
  libffi-dev \
  libssl-dev \
  ""
rm -rf "/home/${USER}/.cargo"
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /root/.cache
rm -rf /usr/share/doc
