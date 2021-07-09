#!/usr/bin/env bash

set -exuo pipefail

# Install Pyston from GitHub .deb
curl -L -o pyston.deb "$PYSTON_DEB"
dpkg -i pyston.deb || true
apt-get install -yf
rm -f pyston.deb

# Set python active
update-alternatives --install /usr/bin/python python /usr/bin/pyston 10
update-alternatives --install /usr/bin/python3 python3 /usr/bin/pyston 10

# Install Pip
curl https://bootstrap.pypa.io/get-pip.py | python
