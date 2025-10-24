#!/bin/sh

rm -f /docker-entrypoint.sh

# Configure Nginx（虽然不使用，但保持目录结构）
mkdir -p /run/nginx
touch /run/nginx/nginx.pid

# Check the environment variables for the flag
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

# 将FLAG写入网站根目录
echo $INSERT_FLAG | tee /var/www/html/flag
chmod 644 /var/www/html/flag

# 安装Java环境
echo "Installing Java runtime..."
apk add --no-cache openjdk8

# 启动JAR文件
cd /var/www/html

echo "Starting shiro-deserialization-ctf.jar..."
# 前台运行，这样容器不会退出
java -jar shiro-deserialization-ctf.jar
