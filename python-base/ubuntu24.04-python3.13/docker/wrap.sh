#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Update APT index
apt-get update

# Run whatever script we're wrapping
bash "$@"

# Clean up APT etc. things from this layer
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /root/.cache
rm -rf /usr/share/doc
