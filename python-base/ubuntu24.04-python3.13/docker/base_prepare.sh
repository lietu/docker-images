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

apt-get upgrade -y
apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
# This line is intentionally empty to preserve trailing \ in previous list
