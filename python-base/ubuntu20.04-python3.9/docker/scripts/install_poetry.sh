#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

POETRY_URL="https://install.python-poetry.org"

mkdir "${POETRY_HOME}"
chown -R "${USER}":"${GROUP}" "${POETRY_HOME}"

su "${USER}" -c "curl -sSL ${POETRY_URL} | python - --version ${POETRY_VERSION}"
# Create the env file manually; installers prior to 1.2.0 created this by default
su "${USER}" -c "echo \"export PATH=\\\"${POETRY_HOME}/bin:\\\$PATH\\\"\" > \"${POETRY_HOME}/env\""

chmod +x "${POETRY_HOME}"/bin/*
bash /src/docker/scripts/configure_poetry.sh
