#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Set up nodesource repository
curl -sL https://deb.nodesource.com/setup_14.x | bash -

# Install Node
apt-get update
apt-get install -y --no-install-recommends nodejs

# Install sane package managers
npm install -g pnpm@7.30.5 yarn
