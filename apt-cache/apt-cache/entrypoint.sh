#!/usr/bin/env bash

apt-cacher-ng
tail --pid=$(pidof apt-cacher-ng) -f /dev/null
