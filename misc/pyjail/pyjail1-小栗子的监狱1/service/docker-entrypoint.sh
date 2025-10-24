#!/bin/bash

echo "=== Starting CTF Challenge ==="

# 设置flag
FLAG="${GZCTF_FLAG:-flag{TEST_Dynamic_FLAG}}"
echo "Setting flag to: $FLAG"

# 创建flag文件
echo "$FLAG" > /flag
echo "Flag file created at /flag"

# 设置权限
chmod 744 /flag

# 验证文件创建
echo "File contents:"
cat /flag
echo "File permissions:"
ls -la /app/flag.txt

# 清理环境变量
unset GZCTF_FLAG

echo "=== Starting PyJail Service ==="

# 通过socat转发Python会话
# TCP4-LISTEN:9999 服务将会转发到9999端口
# reuseaddr 启用端口复用，便于多用户同时连接同一个端口
# [可选]stderr 将脚本的stderr错误输出流也定向到用户会话
socat -v -s TCP4-LISTEN:9999,tcpwrap=script,reuseaddr,fork EXEC:"python3 -u /app/server.py",stderr
