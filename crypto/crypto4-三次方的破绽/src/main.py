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
                                                                               

Silly Bird: Welcome to the RSA Low Exponent Challenge!
I use a very small public exponent (e=3) to encrypt a message.
Your task is to decrypt the message without factoring the modulus.
If you provide the correct decrypted message, I'll give you the flag!
                                                               
'''

def generate_rsa_key():
    """Generate RSA key pair with e=3"""
    # Generate two 1024-bit primes
    p_bits = 1024
    q_bits = 1024
    
    p = next_prime(random.getrandbits(p_bits))
    q = next_prime(random.getrandbits(q_bits))
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use small exponent e=3
    e = 3
    
    # Ensure e and phi are coprime
    while gmpy2.gcd(e, phi) != 1:
        p = next_prime(random.getrandbits(p_bits))
        q = next_prime(random.getrandbits(q_bits))
        n = p * q
        phi = (p - 1) * (q - 1)
    
    # Calculate private key d
    d = gmpy2.invert(e, phi)
    
    return (n, e), (d, p, q)

def generate_random_plaintext(max_bits=None):
    """Generate random plaintext (as integer)"""
    if max_bits:
        # If max_bits is specified, generate a smaller plaintext
        return random.getrandbits(max_bits)
    else:
        # Otherwise generate a regular random number
        return random.getrandbits(256)

def rsa_encrypt(m, public_key):
    """Encrypt message using RSA public key"""
    n, e = public_key
    
    # Ensure message is smaller than n
    if m >= n:
        raise ValueError("Message too long for RSA encryption")
    
    # Encrypt
    c = pow(m, e, n)
    return c

if __name__ == "__main__":
    print(BANNER)
    
    # Generate RSA key pair with e=3
    public_key, private_key = generate_rsa_key()
    n, e = public_key
    d, p, q = private_key
    
    # Generate random plaintext (integer)
    # To ensure low exponent attack works, we need m^3 < n
    # So plaintext bits should be less than n.bit_length()/3
    max_plaintext_bits = n.bit_length() // 3
    original_plaintext = generate_random_plaintext(max_plaintext_bits - 10)  # Leave some margin
    
    # Encrypt message
    ciphertext = rsa_encrypt(original_plaintext, public_key)
    
    # Provide n, e and ciphertext to user
    print(f"\nRSA Public Key:")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"\nEncrypted message (ciphertext):")
    print(f"c = {ciphertext}")
    
    # For development verification - remove this line in production
    #print(f"\n[DEBUG] Original plaintext: {original_plaintext}")
    
    print("\nYour task is to exploit the low exponent vulnerability (e=3)")
    print("and recover the original plaintext.")
    print("Enter the decrypted plaintext (as an integer) below:")
    
    try:
        user_input = input("Decrypted plaintext: ").strip()
        user_plaintext = int(user_input)
        
        # Direct number comparison
        if user_plaintext == original_plaintext:
            print("Congratulations! You successfully exploited the low exponent attack!")
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