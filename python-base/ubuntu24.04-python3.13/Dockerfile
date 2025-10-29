FROM ubuntu-base:24.04

ENV \
    GID=1001 \
    GROUP="api" \
    PATH="${PATH}:/.venv:/usr/local/poetry/bin" \
    POETRY_HOME="/usr/local/poetry" \
    POETRY_VERSION="2.1.4" \
    PYTHONUNBUFFERED=1 \
    PYTHON_VERSION="3.13" \
    UID=1001 \
    USER="api" \
    WORKON_HOME="/.venv" \
    # Workardound for issue with broken virtual environments. For more details see:
    # https://github.com/python-poetry/install.python-poetry.org/blob/main/README.md#debianubuntu
    # https://github.com/python-poetry/poetry/issues/6371#issuecomment-1235764346
    DEB_PYTHON_INSTALL_LAYOUT=deb \
    ENV_LAST_LINE="LEAVE-ME-HERE"

# Run scripts from docker/
WORKDIR /src/
COPY docker/wrap.sh /src/docker/

COPY docker/base_prepare.sh /src/docker/
RUN bash /src/docker/wrap.sh /src/docker/base_prepare.sh

COPY docker/create_user.sh /src/docker/
RUN bash /src/docker/wrap.sh /src/docker/create_user.sh

COPY docker/install_python.sh /src/docker/
RUN bash /src/docker/wrap.sh /src/docker/install_python.sh

COPY docker/prepare_workon_dir.sh /src/docker/
RUN bash /src/docker/wrap.sh /src/docker/prepare_workon_dir.sh

COPY docker/install_poetry.sh /src/docker/
RUN bash /src/docker/wrap.sh /src/docker/install_poetry.sh

RUN rm -rf /src/docker
