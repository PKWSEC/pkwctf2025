import os
import random
import gmpy2
from gmpy2 import mpz, next_prime

flag = os.getenv('GZCTF_FLAG')

BANNER = r'''
                                                             ,----,            
,-.----.           ,--.                                    ,/   .`|            
\    /  \      ,--/  /|            .---.   ,----..       ,`   .'  :     ,---,. 
|   :    \  ,---,': / '           /. ./|  /   /   \    ;    ;     /   ,'  .' | 
|   |  .\ : :   : '/ /        .--'.  ' ; |   :     : .'___,/    ,'  ,---.'   | 
.   :  |: | |   '   ,        /__./ \ : | .   |  ;. / |    :     |   |   |   .' 
|   |   \ : '   |  /     .--'.  '   \' . .   ; /--`  ;    |.';  ;   :   :  :   
|   : .   / |   ;  ;    /___/ \ |    ' ' ;   | ;     `----'  |  |   :   |  |-, 
;   | |`-'  :   '   \   ;   \  \;      : |   : |         '   :  ;   |   :  ;/| 
|   | ;     |   |    '   \   ;  `      | .   | '___      |   |  '   |   |   .' 
:   ' |     '   : |.  \   .   \    .\  ; '   ; : .'|     '   :  |   '   :  '   
:   : :     |   | '_\.'    \   \   ' \ | '   | '/  :     ;   |.'    |   |  |   
|   | :     '   : |         :   '  |--"  |   :    /      '---'      |   :  \   
`---'.|     ;   |,'          \   \ ;      \   \ .'                  |   | ,'   
  `---`     '---'             '---"        `---`                    `----'     
                                                                               

Silly Bird: Welcome to the RSA Challenge!
I will generate a weak RSA key and encrypt a random message.
Your task is to decrypt the message by factoring the modulus n.
If you provide the correct decrypted message, I'll give you the flag!
                                                               
'''

def generate_weak_rsa_key():
    """生成一个弱的RSA密钥对，q非常小"""
    # 生成一个较大的素数p
    p_bits = 1024  # p是正常长度
    p = next_prime(random.getrandbits(p_bits))
    
    # 生成一个非常小的素数q，使得n容易被分解
    q_bits = 20   # q非常小，使得n容易被分解
    q = next_prime(random.getrandbits(q_bits))
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # 选择公钥指数e
    e = 65537
    
    # 计算私钥d
    d = gmpy2.invert(e, phi)
    
    return (n, e), (d, p, q)

def generate_random_plaintext(bits=128):
    """生成随机明文（整数形式）"""
    # 生成一个随机数作为明文，确保它小于n
    return random.getrandbits(bits)

def rsa_encrypt(m, public_key):
    """使用RSA公钥加密消息"""
    n, e = public_key
    
    # 确保消息小于n
    if m >= n:
        raise ValueError("Message too long for RSA encryption")
    
    # 加密
    c = pow(m, e, n)
    return c

if __name__ == "__main__":
    print(BANNER)
    
    # 生成弱RSA密钥对
    public_key, private_key = generate_weak_rsa_key()
    n, e = public_key
    d, p, q = private_key
    
    # 生成随机明文（整数）
    original_plaintext = generate_random_plaintext()
    
    # 加密消息
    ciphertext = rsa_encrypt(original_plaintext, public_key)
    
    # 给用户提供n、e和密文
    print(f"\nRSA Public Key:")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"\nEncrypted message (ciphertext):")
    print(f"c = {ciphertext}")
    
    # 开发时用于验证 - 正式使用时请删除下面这行
    #print(f"\n[DEBUG] Original plaintext: {original_plaintext}")
    
    print("\nYour task is to factor n and decrypt the message.")
    print("Enter the decrypted plaintext (as an integer) below:")
    
    try:
        user_input = input("Decrypted plaintext: ").strip()
        user_plaintext = int(user_input)
        
        # 直接比较数字，不进行字符串比较
        if user_plaintext == original_plaintext:
            print("Congratulations! You successfully decrypted the message!")
            print(f"Here is your flag: {flag}")
        else:
            print("Wrong! The decrypted plaintext is incorrect.")
            print("Program exiting...")
            
    except ValueError:
        print("Error: Please enter a valid integer.")
        print("Program exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Program exiting...")