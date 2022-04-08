#!/usr/bin/env bash

apt-cacher-ng
devpi-server --serverdir /cache/.devpi/server --listen 0.0.0.0:3141
