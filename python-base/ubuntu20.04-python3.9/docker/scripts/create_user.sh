#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Create user
addgroup --system --gid "${GID}" "${GROUP}"
useradd \
  --uid "${UID}" \
  --shell /bin/bash \
  --gid "${GID}" \
  --create-home \
  "${USER}"
