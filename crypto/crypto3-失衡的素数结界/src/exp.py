#!/usr/bin/env python3
import gmpy2
import binascii

def rsa_decrypt_with_factors(p, q, e, c):
    """
    使用已知的p和q解密密文c
    """
    # 计算n
    n = p * q
    print(f"n = {n}")
    
    # 计算φ(n)
    phi = (p - 1) * (q - 1)
    print(f"φ(n) = {phi}")
    
    # 计算私钥d
    d = gmpy2.invert(e, phi)
    print(f"d = {d}")
    
    # 解密密文
    m_int = pow(c, d, n)
    print(f"解密后的整数: {m_int}")
    
    # 将整数转换为字符串
    try:
        hex_str = hex(m_int)[2:]
        if len(hex_str) % 2:
            hex_str = '0' + hex_str
        decrypted = binascii.unhexlify(hex_str).decode('utf-8')
        print(f"解密后的消息: {decrypted}")
        return decrypted
    except Exception as e:
        print(f"转换为字符串时出错: {e}")
        # 如果解码失败，返回整数形式
        return str(m_int)

def main():
    print("=== RSA 半自动解密工具 ===")
    print("请按照以下步骤操作:")
    print("1. 从服务器获取n、e和c的值")
    print("2. 使用在线工具（如factordb.com）分解n得到p和q")
    print("3. 将p、q、e和c的值输入到本工具中")
    print("4. 本工具将计算出明文m")
    print("5. 将明文m手动输入到服务器中获取flag")
    print()
    
    # 获取用户输入
    try:
        p = int(input("请输入p的值: ").strip())
        q = int(input("请输入q的值: ").strip())
        e = int(input("请输入e的值: ").strip())
        c = int(input("请输入c的值: ").strip())
    except ValueError:
        print("输入错误，请确保输入的是有效的整数")
        return
    
    # 验证p和q
    n = p * q
    print(f"\n验证: p * q = {p} * {q} = {n}")
    
    # 解密密文
    print("\n开始解密...")
    decrypted_message = rsa_decrypt_with_factors(p, q, e, c)
    
    print(f"\n=== 解密结果 ===")
    print(f"明文 m = '{decrypted_message}'")
    print("\n请将上面的明文手动输入到服务器中")

if __name__ == "__main__":
    main()
