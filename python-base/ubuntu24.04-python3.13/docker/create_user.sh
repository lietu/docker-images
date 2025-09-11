#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Create user
groupadd --system --gid "${GID}" "${GROUP}"

useradd \
  --uid "${UID}" \
  --shell /bin/bash \
  --gid "${GID}" \
  --create-home \
  "${USER}"

# Allow the next scripts to run as ${USER}
chown -R "${USER}":"${GROUP}" /src
