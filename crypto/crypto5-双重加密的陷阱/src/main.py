import os
import random
import gmpy2
from gmpy2 import mpz, next_prime, gcdext

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
                                                                               

Silly Bird: Welcome to the RSA Challenge 3!
I encrypted the same message with two different public exponents but the same modulus.
Your task is to recover the original message using the common modulus attack.
If you provide the correct decrypted message, I'll give you the flag!
                                                               
'''

def generate_rsa_key():
    """Generate RSA key pair with two different public exponents"""
    # Generate two 1024-bit primes
    p_bits = 1024
    q_bits = 1024
    
    p = next_prime(random.getrandbits(p_bits))
    q = next_prime(random.getrandbits(q_bits))
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use two different 4-digit public exponents
    e1 = 0
    e2 = 0
    
    # Ensure both exponents are coprime with phi and with each other
    while True:
        e1 = random.randint(1000, 9999)
        e2 = random.randint(1000, 9999)
        
        if (gmpy2.gcd(e1, phi) == 1 and 
            gmpy2.gcd(e2, phi) == 1 and 
            gmpy2.gcd(e1, e2) == 1):
            break
    
    # Calculate private keys
    d1 = gmpy2.invert(e1, phi)
    d2 = gmpy2.invert(e2, phi)
    
    return (n, e1, e2), (d1, d2, p, q)

def generate_random_plaintext(max_bits=None):
    """Generate random plaintext (as integer)"""
    if max_bits:
        # If max_bits is specified, generate a smaller plaintext
        return random.getrandbits(max_bits)
    else:
        # Otherwise generate a regular random number
        return random.getrandbits(256)

def rsa_encrypt(m, n, e):
    """Encrypt message using RSA with given n and e"""
    # Ensure message is smaller than n
    if m >= n:
        raise ValueError("Message too long for RSA encryption")
    
    # Encrypt
    c = pow(m, e, n)
    return c

if __name__ == "__main__":
    print(BANNER)
    
    # Generate RSA key pair with two different public exponents
    public_key, private_key = generate_rsa_key()
    n, e1, e2 = public_key
    d1, d2, p, q = private_key
    
    # Generate random plaintext (integer)
    original_plaintext = generate_random_plaintext()
    
    # Encrypt message with both public exponents
    ciphertext1 = rsa_encrypt(original_plaintext, n, e1)
    ciphertext2 = rsa_encrypt(original_plaintext, n, e2)
    
    # Provide n, e1, e2 and both ciphertexts to user
    print(f"\nRSA Public Key:")
    print(f"n = {n}")
    print(f"e1 = {e1}")
    print(f"e2 = {e2}")
    print(f"\nEncrypted messages (ciphertexts):")
    print(f"c1 = {ciphertext1}")
    print(f"c2 = {ciphertext2}")
    
    # For development verification - remove this line in production
    #print(f"\n[DEBUG] Original plaintext: {original_plaintext}")
    
    print("\nYour task is to exploit the common modulus vulnerability")
    print("and recover the original plaintext.")
    print("Enter the decrypted plaintext (as an integer) below:")
    
    try:
        user_input = input("Decrypted plaintext: ").strip()
        user_plaintext = int(user_input)
        
        # Direct number comparison
        if user_plaintext == original_plaintext:
            print("Congratulations! You successfully exploited the common modulus attack!")
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