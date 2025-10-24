#!/bin/bash
set -e

# --- GZCTF 动态 Flag 处理 ---
if [ -n "$GZCTF_FLAG" ]; then
    FLAG1=$(echo "$GZCTF_FLAG" | cut -d',' -f1)
    FLAG2=$(echo "$GZCTF_FLAG" | cut -d',' -f2)
    FLAG3=$(echo "$GZCTF_FLAG" | cut -d',' -f3)

    echo "$FLAG1" > /flag1.txt
    echo "$FLAG2" > /flag2.txt
    echo "$FLAG3" > /flag

    chmod 444 /flag1.txt
    chmod 444 /flag2.txt
    chmod 400 /flag

    unset GZCTF_FLAG
else
    # 默认静态 flag（本地调试用）
    echo "flag{we1c0me~~ple@se_cont1nue}" > /flag1.txt
    echo "flag{ok~y0u_w1n~you_can_go?}" > /flag2.txt
    echo "flag{f1nal!!!!!winer!!}" > /flag
    chmod 444 /flag1.txt
    chmod 444 /flag2.txt
    chmod 400 /flag
fi

# 启动 Spring Boot 应用，强制绑定 8833
exec su ctf -c "cd /app && java -jar app.jar --server.port=8833"