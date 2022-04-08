#!/usr/bin/env sh

if [ ! -z "${APT_CACHE:-}" ]; then
  echo 'Acquire::http::Proxy "http://'"${APT_CACHE}"':3142;' > /etc/apt/apt.conf.d/02proxy
  echo 'Acquire::https::Proxy "http://'"${APT_CACHE}"':3142;' >> /etc/apt/apt.conf.d/02proxy
fi
