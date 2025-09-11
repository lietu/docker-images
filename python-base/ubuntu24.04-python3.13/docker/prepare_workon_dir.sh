#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Ensure the WORKON_HOME exists, is empty and owned by ${USER}
if [[ ! -d "${WORKON_HOME}" ]]; then
  mkdir "${WORKON_HOME}"
fi
rm -rf "${WORKON_HOME:?}"/*
chown -R "${USER}":"${GROUP}" "${WORKON_HOME}"
