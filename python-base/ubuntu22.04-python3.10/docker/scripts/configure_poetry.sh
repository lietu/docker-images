#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

su "${USER}" -c ". ${POETRY_HOME}/env; poetry config virtualenvs.in-project false"
su "${USER}" -c ". ${POETRY_HOME}/env; poetry config virtualenvs.path ${WORKON_HOME}"
#su "${USER}" -c ". ${POETRY_HOME}/env; poetry config experimental.new-installer false"
