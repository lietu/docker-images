FROM python-base:ubuntu22.04-python3.10

ENV PATH="/home/api/.cargo/bin:$PATH"

USER ${USER}

RUN : \
 && set -exu \
 && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y \
 && :

USER root
