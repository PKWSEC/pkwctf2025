FROM php:7.3-fpm-alpine3.11

ARG http_proxy
ARG https_proxy
ARG no_proxy

ADD repositories /etc/apk/repositories
ADD default.conf /
ADD index.php /
ADD run.sh /
RUN apk update && apk add nginx && \
    apk add m4 autoconf make gcc g++ linux-headers && \
    docker-php-ext-install pdo_mysql opcache mysqli && \
    mkdir /run/nginx && \
    mv /default.conf /etc/nginx/conf.d && \
    mv /index.php /var/www/html && \
    touch /run/nginx/nginx.pid && \
    chmod 755 /run.sh && \
    chmod 755 /var/www/html/ &&\
    apk del m4 autoconf make gcc g++ linux-headers

EXPOSE 80

ENTRYPOINT ["/run.sh"]
