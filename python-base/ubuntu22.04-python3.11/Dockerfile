ARG LOCAL_REGISTRY=""
FROM ${LOCAL_REGISTRY}ubuntu-base:20.04

ENV \
    GID=1000 \
    GROUP="api" \
    PATH="${PATH}:/.venv:/usr/local/poetry/bin" \
    POETRY_HOME="/usr/local/poetry" \
    POETRY_VERSION="1.5.1" \
    PYTHONUNBUFFERED=1 \
    PYTHON_VERSION="3.11" \
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
