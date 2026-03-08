#!/bin/sh
set -eu

NGINX_PORT="${NGINX_PORT:-80}"

case "$NGINX_PORT" in
  ''|*[!0-9]*)
    echo "NGINX_PORT must be a number, got: $NGINX_PORT" >&2
    exit 1
    ;;
esac

if [ "$NGINX_PORT" -lt 1 ] || [ "$NGINX_PORT" -gt 65535 ]; then
  echo "NGINX_PORT must be between 1 and 65535, got: $NGINX_PORT" >&2
  exit 1
fi

sed "s/__NGINX_PORT__/$NGINX_PORT/g" /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec "$@"
