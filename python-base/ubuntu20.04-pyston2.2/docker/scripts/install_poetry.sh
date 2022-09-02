#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

POETRY_URL="https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py"

mkdir "${POETRY_HOME}"
chown -R "${USER}":"${GROUP}" "${POETRY_HOME}"

su "${USER}" -c "curl -sSL ${POETRY_URL} -o /tmp/get-poetry.py"
su "${USER}" -c "python /tmp/get-poetry.py --version ${POETRY_VERSION}"

chmod +x "${POETRY_HOME}"/bin/*
bash /src/docker/scripts/configure_poetry.sh

# Remove useless old vendor packages
cd /usr/local/poetry/lib/poetry/_vendor/
KEEP="py${PYTHON_VERSION}"
for dir in py*; do
  if [[ ! $KEEP =~ (^|[[:space:]])$dir($|[[:space:]]) ]]; then
    rm -rf "${dir}"
  fi
done
cd -
