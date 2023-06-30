#!/usr/bin/env bash

# shellcheck disable=SC2039
set -exuo pipefail

# Install pipx
python3.10 -m pip install --user -U pipx
/root/.local/bin/pipx ensurepath
export PATH="/root/.local/bin:$PATH"

# Install multi-start
pipx install multi-start
