import os
import random
import string
import base64

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
                                                                               

Silly Bird: Welcome to the Encoding Challenge!
I created a random string and encoded it 5 times.
Your task is to decode it back to the original string.
If you provide the correct original string, I'll give you the flag!
                                                               
'''

def generate_random_string(length=20):
    """Generate random string"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def encode_base64_multiple_times(text, times=5):
    """Encode text multiple times with base64"""
    encoded = text
    for _ in range(times):
        encoded = base64.b64encode(encoded.encode()).decode()
    return encoded

if __name__ == "__main__":
    print(BANNER)
    
    # Generate random string
    original_string = generate_random_string()
    
    # Encode 5 times with base64
    encoded_string = encode_base64_multiple_times(original_string, 5)
    
    # Output encoded string
    print(f"Encoded string:")
    print(f"{encoded_string}")
    
    # For development verification - remove this line in production
    
    print("\nYour task is to decode this string back to the original.")
    print("Enter the decoded original string below:")
    
    try:
        user_input = input("Original string: ").strip()
        
        # Direct string comparison
        if user_input == original_string:
            print("Congratulations! You successfully decoded the base64 layers!")
            print(f"Here is your flag: {flag}")
        else:
            print("Wrong! The decoded string is incorrect.")
            print("Program exiting...")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Program exiting...")
