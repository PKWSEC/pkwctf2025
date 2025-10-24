import os

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
                                                                               

Silly Bird: Welcome to ECC Challenge 2!
Do u know Pohlig-Hellman attack?
Find the scalar k such that Q = k * P.
If you solve this challenge, I'll give you the flag!
'''

def ecc_challenge():
    p = 1325416721508058184199521259248902139850404903851597997
    A = 438144801358559866330118056730491044114357230217832105
    B = 475060046171787304780239042127285096307868115005374593
    
    # Create the elliptic curve
    E = EllipticCurve(GF(p), [A, B])
    
    # Use a fixed generator point P instead of a random point
    # We'll use the first point we find on the curve as the generator
    # In practice, you might want to choose a specific generator
    P = E.gen(0)  # Use the first generator of the curve
    
    # Generate a random scalar k
    k = randint(1, p-1)
    
    # Compute Q = k * P
    Q = k * P
    
    return {
        'p': p,
        'A': A,
        'B': B,
        'P': P.xy(),
        'Q': Q.xy(),
        'k': k
    }

if __name__ == "__main__":
    print(BANNER)
    
    # Generate the challenge
    challenge = ecc_challenge()
    
    print(f"Curve parameters:")
    print(f"p = {challenge['p']}")
    print(f"A = {challenge['A']}")
    print(f"B = {challenge['B']}")
    print(f"Point P = {challenge['P']}")
    print(f"Point Q = {challenge['Q']}")
    print(f"\nYour task is to find the scalar k such that Q = k * P")
    
    # For development verification - remove this line in production
    # print(f"\n[DEBUG] Expected answer: {challenge['k']}")
    
    try:
        user_input = input(f"\nEnter the solution k: ").strip()
        user_answer = int(user_input)
        
        if user_answer == challenge['k']:
            print("Correct!")
            print(f"Here is your flag: {flag}")
        else:
            print(f"Wrong! The correct answer was {challenge['k']}.")
            print("Program exiting...")
            
    except ValueError:
        print("Error: Please enter a valid integer.")
        print("Program exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Program exiting...")