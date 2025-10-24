#!/bin/sh
set -e

# 防止被重复执行（build 时会复制进镜像，所以首次运行需要删除）
rm -f /docker-entrypoint.sh || true

# ========== FLAG 注入（保留你的逻辑） ==========
if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
    export DASFLAG=no_FLAG
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
    export FLAG=no_FLAG
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
    export GZCTF_FLAG=no_FLAG
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi
echo "$INSERT_FLAG" | tee /flag
chmod 744 /flag

# ========== MariaDB 初始化 (只在首次数据目录为空时进行) ==========
DATADIR="/var/lib/mysql"

if [ ! -d "$DATADIR/mysql" ]; then
    echo "[entrypoint] Initializing MariaDB data directory..."
    mysql_install_db --user=mysql --datadir="$DATADIR" > /dev/null 2>&1 || true
fi

# 启动 mysqld（后台）
echo "[entrypoint] Starting mysqld..."
# 使用 --skip-networking=0 保持可通过 TCP 本地访问（CMS 通过 127.0.0.1 连接）
mysqld --user=mysql --datadir="$DATADIR" --socket=/var/run/mysqld/mysqld.sock --skip-networking=0 &

# 等待 mysqld 可用
MAX_WAIT=30
i=0
while ! mysqladmin ping --silent >/dev/null 2>&1; do
    i=$((i+1))
    if [ $i -ge $MAX_WAIT ]; then
        echo "mysqld failed to start within $MAX_WAIT seconds" >&2
        exit 1
    fi
    sleep 1
done
echo "[entrypoint] mysqld is up."

# ========== 确保数据库和账户存在（按你给出的配置信息） ==========
# DB: seacms, user: root, pass: root
# 注意：我们把 root@localhost 密码设置为 root，方便 CMS 直接连接
mysql -uroot <<SQL
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS seacms DEFAULT CHARSET utf8;
GRANT ALL PRIVILEGES ON seacms.* TO 'root'@'localhost' IDENTIFIED BY 'root';
FLUSH PRIVILEGES;
SQL

# 导入 seacms 初始 SQL（如果存在），容错处理
if [ -f /docker-entry.sql ]; then
    echo "[entrypoint] Importing /docker-entry.sql -> seacms"
    mysql -uroot -proot seacms < /docker-entry.sql || echo "[entrypoint] import returned non-zero (ignored)"
fi

# ========== 启动 php-fpm 与 nginx ==========
echo "[entrypoint] Starting php-fpm and nginx..."
# php-fpm 已在基础镜像提供，直接后台启动
php-fpm &

# 确保 nginx 日志目录存在
mkdir -p /var/log/nginx
touch /var/log/nginx/access.log /var/log/nginx/error.log

# 启动 nginx (前台)
nginx -g "daemon off;" &

echo "Seacms CMS (PHP7.3.4) with embedded DB started."

# 输出日志到控制台，方便调试（阻塞）
tail -F /var/log/nginx/access.log /var/log/nginx/error.log
