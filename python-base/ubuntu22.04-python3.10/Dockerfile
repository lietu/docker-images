FROM lietu/ubuntu-base:22.04

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
    PYTHON_VERSION="3.10" \
    TZ="UTC" \
    UID=1000 \
    USER="api" \
    WORKON_HOME="/.venv" \
    # Workardound for issue with broken virtual environments. For more details see:
    # https://github.com/python-poetry/install.python-poetry.org/blob/main/README.md#debianubuntu
    # https://github.com/python-poetry/poetry/issues/6371#issuecomment-1235764346
    DEB_PYTHON_INSTALL_LAYOUT=deb \
    ENV_LAST_LINE="LEAVE-ME-HERE"

# Run docker/base-prepare.sh
WORKDIR /src/
COPY docker /src/docker
RUN : \
 && set -exu \
 && bash /src/docker/base-prepare.sh \
 && rm -rf /src/docker \
 && :
