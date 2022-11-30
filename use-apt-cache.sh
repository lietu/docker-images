#!/usr/bin/env sh

# Will enable APT cache proxy if APT_CACHE env variable is set to the hostname of the cache server
# Will also disable HTTPS for all sources for caching to work, make sure you have rewrites in place
#
# Usage:
#   curl https://raw.githubusercontent.com/lietu/docker-images/master/use-apt-cache.sh | sudo sh -

if [ -n "${APT_CACHE:-}" ]; then
  echo 'Acquire::http::Proxy "http://'"${APT_CACHE}"':3142";' > /etc/apt/apt.conf.d/02proxy
  echo 'Acquire::https::Proxy "http://'"${APT_CACHE}"':3142";' >> /etc/apt/apt.conf.d/02proxy

  sed -Ei 's@https://@http://@g' /etc/apt/sources.list
  if find /etc/apt/sources.list.d -name "*.list" 2>/dev/null | grep -q .; then
    sed -Ei 's@https://@http://@g' /etc/apt/sources.list.d/*.list
  fi
fi
