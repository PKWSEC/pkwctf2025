#!/usr/bin/env python3
from pwn import *
import math

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def euler_phi(n):
    if n <= 0:
        return 0
    factors = factorize(n)
    result = n
    for p in factors:
        result *= (p - 1)
        result //= p
    return result

def solve():
    conn = remote('ctf.pkwsec.com', 32809)

    for i in range(10):
        # 等待"Number "，然后接收该行
        conn.recvuntil(b'Number ')
        # 接收该行的剩余部分，格式为 "i: xxxx"
        line = conn.recvline().decode().strip()
        # 提取数字，注意line的格式是 "i: xxxx"
        n = int(line.split(': ')[1])
        print(f"Number {i+1}: {n}")

        # 计算答案
        answer = euler_phi(n)
        print(f"φ({n}) = {answer}")

        # 等待提示输入
        # 注意：提示字符串是 "Please enter φ(n): "，其中n是数字
        conn.recvuntil(f'Please enter φ({n}): '.encode())

        # 发送答案
        conn.sendline(str(answer).encode())

        # 接收响应
        response = conn.recvline().decode()
        print(f"Response: {response}")

        # 检查是否正确
        if "Correct" not in response:
            print("Wrong answer! Exiting...")
            break
        # 如果是最后一个数字，接下来就是flag
        if i == 9:
            # 接收flag
            conn.recvuntil(b'flag: ')
            flag = conn.recvline().decode().strip()
            print(f"Flag: {flag}")

    conn.close()

if __name__ == '__main__':
    solve()
