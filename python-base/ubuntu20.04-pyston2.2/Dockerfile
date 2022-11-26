FROM lietu/ubuntu-base:20.04

ENV \
    DEBIAN_FRONTEND="noninteractive" \
    GID=1000 \
    GROUP="api" \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="${PATH}:/.venv:/usr/local/poetry/bin" \
    POETRY_HOME="/usr/local/poetry" \
    POETRY_VERSION="1.2.0" \
    PYTHONUNBUFFERED=1 \
    PYTHON_VERSION="3.8" \
    PYSTON_DEB="https://github.com/pyston/pyston/releases/download/pyston_2.2/pyston_2.2_20.04.deb" \
    TZ="UTC" \
    UID=1000 \
    USER="api" \
    WORKON_HOME="/.venv" \
    ENV_LAST_LINE="LEAVE-ME-HERE"

# Run docker/base-prepare.sh
WORKDIR /src/
COPY docker /src/docker
RUN : \
 && set -exu \
 && bash /src/docker/base-prepare.sh \
 && rm -rf /src/docker \
 && :
