#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Deadsnakes PPA is the only way to get stable Python 3.11 for Ubuntu 22.04
apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y

# Install python
apt-get install -y --no-install-recommends \
  "python${PYTHON_VERSION}" \
  "python${PYTHON_VERSION}-venv" \
  python3-distutils

# Set python active
update-alternatives --install /usr/bin/python python "/usr/bin/python${PYTHON_VERSION}" 10

# Install Pip
curl https://bootstrap.pypa.io/get-pip.py | python
