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
apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
# This line is intentionally empty to preserve trailing \ in previous list

bash /src/docker/scripts/install_node.sh

# Allow the next script to run as ${USER}
chown -R "${USER}":"${GROUP}" /src

# Cleanup
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /root/.cache
rm -rf /usr/share/doc
