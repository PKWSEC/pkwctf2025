FROM php:7.3.4-fpm-alpine

LABEL auther_template="CTF-Archives"

# 切换镜像源并安装 nginx bash mariadb (server + client) 以及 php-mysql 扩展
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
  && apk add --no-cache nginx bash mariadb mariadb-client \
  && docker-php-ext-install pdo pdo_mysql mysqli \
  && mkdir -p /var/run/nginx

# 复制入口脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 复制 nginx 配置
COPY ./config/nginx.conf /etc/nginx/nginx.conf

# 复制 web 项目 (CMS 源码)
COPY src /var/www/html
RUN chown -R www-data:www-data /var/www/html

# 把 DB 初始化 SQL 放进镜像（你需提供该文件）
# 放在 ./config/seacms.sql
COPY ./config/seacms.sql /docker-entry.sql

WORKDIR /var/www/html

# 暴露 HTTP 端口；不要暴露 3306（数据库只在容器内部可访问）
EXPOSE 80

VOLUME ["/var/log/nginx"]

ENTRYPOINT ["/docker-entrypoint.sh"]
