#!/bin/sh
set -eu

# Start MySQL in the background
mysqld_safe &

# --- Wait for MySQL to be ready ---
echo "Waiting for MySQL to start..."
for i in $(seq 1 30); do
    if mysqladmin ping -uroot -proot --silent 2>/dev/null; then
        echo "MySQL started successfully."
        break
    fi
    echo "Waiting for MySQL... attempt $i/30"
    sleep 1
done

# Check if MySQL is really ready
if ! mysqladmin ping -uroot -proot --silent 2>/dev/null; then
    echo "ERROR: MySQL failed to start within 30 seconds"
    exit 1
fi

# --- Setup Databases and Tables ---
echo "Creating databases..."
mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS ctf;" 2>/dev/null
mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS secret;" 2>/dev/null

echo "Importing SQL files..."
[ -f /var/ctf.sql ] && mysql -uroot -proot -D ctf < /var/ctf.sql 2>/dev/null
[ -f /var/secret.sql ] && mysql -uroot -proot -D secret < /var/secret.sql 2>/dev/null

# --- Populate flag parts (split into three parts and place accordingly) ---
if [ -n "${GZCTF_FLAG:-}" ]; then
    echo "Processing flag of length: ${#GZCTF_FLAG}"
    gz_flag="$GZCTF_FLAG"
    length=${#gz_flag}
    part_length=$((length / 3))

    # 确保分割准确，处理不能整除的情况
    part1=$(echo -n "$gz_flag" | cut -c1-$part_length)
    part2_start=$((part_length + 1))
    part2_end=$((2 * part_length))
    part2=$(echo -n "$gz_flag" | cut -c$part2_start-$part2_end)
    part3_start=$((2 * part_length + 1))
    part3=$(echo -n "$gz_flag" | cut -c$part3_start-)

    echo "Flag parts:"
    echo "Part1 (${#part1} chars): ${part1}"
    echo "Part2 (${#part2} chars): ${part2}"
    echo "Part3 (${#part3} chars): ${part3}"

    echo "Updating flags in database..."
    # 更新secret数据库
    mysql -uroot -proot -e "USE secret; UPDATE password SET flag = '$part1' WHERE id = '1' LIMIT 1;" 2>/dev/null
    
    # 更新ctf数据库
    mysql -uroot -proot -e "USE ctf; UPDATE score SET grade = '$part2' WHERE student = 'pkwsec' LIMIT 1;" 2>/dev/null

    # 写入文件
    echo -n "$part3" > /flag
    echo "Third flag part written to /flag"

    # 验证写入
    echo "Verifying writes..."
    secret_flag=$(mysql -uroot -proot -N -e "USE secret; SELECT flag FROM password WHERE id='1' LIMIT 1;" 2>/dev/null)
    ctf_flag=$(mysql -uroot -proot -N -e "USE ctf; SELECT grade FROM score WHERE student='pkwsec' LIMIT 1;" 2>/dev/null)
    file_flag=$(cat /flag 2>/dev/null || echo "file_read_error")
    
    echo "Secret DB flag part: $secret_flag"
    echo "CTF DB flag part: $ctf_flag"
    echo "File flag part: $file_flag"

else
    echo "WARNING: GZCTF_FLAG environment variable not set. Using placeholder flags."
    mysql -uroot -proot -e "USE secret; UPDATE password SET flag = 'PKWCTF{y0u' WHERE id = '1' LIMIT 1;" 2>/dev/null
    mysql -uroot -proot -e "USE ctf; UPDATE score SET grade = '-g3t-1t' WHERE student = 'pkwsec' LIMIT 1;" 2>/dev/null
    printf '%s' '-s0-c00l}' > /flag
fi

# Clear sensitive env (remove variables)
unset GZCTF_FLAG || true

# --- Start Apache in foreground ---
echo "Starting Apache..."
exec apache2-foreground
