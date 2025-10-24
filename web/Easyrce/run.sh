#!/bin/sh
set -eu

echo "$GZCTF_FLAG" > /f14g
chmod 444 /f14g

unset GZCTF_FLAG

php-fpm -D
exec nginx -g 'daemon off;'