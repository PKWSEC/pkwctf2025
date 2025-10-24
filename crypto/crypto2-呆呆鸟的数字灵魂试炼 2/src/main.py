import os
import random
import gmpy2
import signal
import sys
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
                                                                               

Silly Bird:I will show you 10 numbers one by one.
For each number, you need to calculate φ(n) and enter your answer.
If you get any answer wrong, the program will exit immediately.

(Generating the questions, please wait a moment.)
                                                               
'''

def generate_random_numbers():
    """生成10个随机且不同量级的数字"""
    numbers = []
    
    # 1. 小质数 (10-100)
    small_prime = next_prime(random.randint(10, 100))
    numbers.append(small_prime)
    
    # 2. 中等质数 (100-1000)
    medium_prime = next_prime(random.randint(100, 1000))
    numbers.append(medium_prime)
    
    # 3. 两个小质数的乘积
    p1 = next_prime(random.randint(10, 50))
    p2 = next_prime(random.randint(50, 100))
    numbers.append(p1 * p2)
    
    # 4. 质数的平方
    base_prime = next_prime(random.randint(5, 20))
    numbers.append(base_prime * base_prime)
    
    # 5. 三个不同质数的乘积
    p3 = next_prime(random.randint(2, 10))
    p4 = next_prime(random.randint(10, 20))
    p5 = next_prime(random.randint(20, 30))
    numbers.append(p3 * p4 * p5)
    
    # 6. 较大的质数 (1000-10000)
    large_prime = next_prime(random.randint(1000, 10000))
    numbers.append(large_prime)
    
    # 7. 两个较大质数的乘积
    p6 = next_prime(random.randint(100, 500))
    p7 = next_prime(random.randint(500, 1000))
    numbers.append(p6 * p7)
    
    # 8. 质数的立方
    cube_base = next_prime(random.randint(5, 15))
    numbers.append(cube_base * cube_base * cube_base)
    
    # 9. 四个质数的乘积
    p8 = mpz(2)
    p9 = next_prime(random.randint(3, 10))
    p10 = next_prime(random.randint(10, 20))
    p11 = next_prime(random.randint(20, 30))
    numbers.append(p8 * p9 * p10 * p11)
    
    # 10. 更大的质数乘积
    p12 = next_prime(random.randint(1000, 5000))
    p13 = next_prime(random.randint(5000, 10000))
    numbers.append(p12 * p13)
    
    return numbers

def euler_totient(n):
    """计算欧拉函数φ(n)"""
    # 使用gmpy2的gcd函数和手动计算欧拉函数
    result = mpz(1)
    if n > 1:
        result = mpz(0)
        for i in range(1, n):
            if gmpy2.gcd(i, n) == 1:
                result += 1
    return result

def timeout_handler(signum, frame):
    """超时处理函数"""
    print("\n\nTime's up! You took too long to answer all questions.")
    print("Program exiting...")
    sys.exit(1)

if __name__ == "__main__":
    print(BANNER)
    
    # 生成随机数字
    numbers = generate_random_numbers()
    correct_answers = [int(euler_totient(n)) for n in numbers]
    
    # 设置超时处理
    signal.signal(signal.SIGALRM, timeout_handler)
    
    correct_count = 0
    
    for i, num in enumerate(numbers, 1):
        print(f"Number {i}: {num}")
        
        # 如果是第一个数字，开始计时
        if i == 1:
            print("Timer started! You have 5 seconds to complete all 10 questions.")
            signal.alarm(5)  # 5秒后触发超时
        
        try:
            user_answer = int(input(f"Please enter φ({num}): ").strip())
            
            if user_answer == correct_answers[i-1]:
                print("Correct!\n")
                correct_count += 1
            else:
                print(f"Wrong! The correct answer is {correct_answers[i-1]}.")
                print("Program exiting...")
                signal.alarm(0)  # 取消定时器
                exit(1)
                
        except ValueError:
            print("Error: Please enter a valid integer.")
            print("Program exiting...")
            signal.alarm(0)  # 取消定时器
            exit(1)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            signal.alarm(0)  # 取消定时器
            exit(1)
    
    # 如果所有答案都正确，取消定时器并显示flag
    signal.alarm(0)
    if correct_count == 10:
        print("Congratulations! You answered all 10 questions correctly!")
        print(f"Here is your flag: {flag}")