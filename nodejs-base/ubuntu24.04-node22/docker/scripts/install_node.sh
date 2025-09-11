#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Set up node
NODE_MAJOR=22

# Prepare nodesource keyring
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# Set up repository
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

# Install Node
apt-get update
apt-get install -y --no-install-recommends nodejs

# Install sane package managers
npm install -g pnpm yarn bun
