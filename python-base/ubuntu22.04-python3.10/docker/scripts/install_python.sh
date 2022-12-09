#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Install python
apt-get install -y --no-install-recommends \
  "python${PYTHON_VERSION}" \
  "python${PYTHON_VERSION}-venv" \
  python3-distutils

# Set python active
update-alternatives --install /usr/bin/python python "/usr/bin/python${PYTHON_VERSION}" 10

# Install Pip
curl https://bootstrap.pypa.io/get-pip.py | python
