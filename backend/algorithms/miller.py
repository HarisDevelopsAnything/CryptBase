import random

def miller_rabin_with_steps(n, k):
    """
    Miller-Rabin primality test with detailed steps
    
    Args:
        n: The number to test for primality
        k: The number of iterations (witnesses to test)
    
    Returns:
        dict: Contains isPrime boolean and steps list
    """
    steps = []
    
    # Step 1: Check edge cases
    if n <= 1:
        steps.append({
            'step': 1,
            'description': f'Number {n} is <= 1',
            'result': 'Not prime (numbers <= 1 are not prime)'
        })
        return {'isPrime': False, 'steps': steps}
    
    if n <= 3:
        steps.append({
            'step': 1,
            'description': f'Number {n} is 2 or 3',
            'result': 'Prime (2 and 3 are prime)'
        })
        return {'isPrime': True, 'steps': steps}
    
    if n % 2 == 0:
        steps.append({
            'step': 1,
            'description': f'Number {n} is even',
            'result': 'Not prime (even numbers except 2 are not prime)'
        })
        return {'isPrime': False, 'steps': steps}
    
    # Step 2: Write n-1 as 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    steps.append({
        'step': 1,
        'description': f'Express n-1 as 2^r × d',
        'calculation': f'{n}-1 = {n-1} = 2^{r} × {d}',
        'result': f'r = {r}, d = {d}'
    })
    
    # Step 3-k+2: Test k random witnesses
    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        
        step_num = i + 2
        
        steps.append({
            'step': step_num,
            'description': f'Iteration {i+1}: Testing with witness a = {a}',
            'calculation': f'x = {a}^{d} mod {n} = {x}',
            'result': ''
        })
        
        if x == 1 or x == n - 1:
            steps.append({
                'step': step_num,
                'description': f'Initial check',
                'result': f'✓ Passed (x = {x}, which is 1 or n-1)'
            })
            continue
        
        # Square x repeatedly r-1 times
        composite_found = True
        for j in range(r - 1):
            x = pow(x, 2, n)
            
            steps.append({
                'step': step_num,
                'description': f'  Squaring iteration {j+1}/{r-1}',
                'calculation': f'x = x^2 mod {n} = {x}',
                'result': ''
            })
            
            if x == n - 1:
                steps.append({
                    'step': step_num,
                    'description': f'  Check result',
                    'result': f'✓ Passed (x = {x} = n-1)'
                })
                composite_found = False
                break
        
        if composite_found:
            steps.append({
                'step': step_num,
                'description': f'  Final check',
                'result': f'✗ Failed (x never became n-1)'
            })
            steps.append({
                'step': step_num + 1,
                'description': 'Conclusion',
                'result': f'{n} is definitely composite (not prime)'
            })
            return {'isPrime': False, 'steps': steps}
    
    # All tests passed
    steps.append({
        'step': k + 2,
        'description': 'Conclusion',
        'result': f'All {k} iterations passed. {n} is probably prime with probability ≥ 1 - (1/4)^{k}'
    })
    
    return {'isPrime': True, 'steps': steps}

def millerTest(n,k):
    if n<=1:
        return False
    if n<=3:
        return True
    if n%2==0:
        return False
    r=0
    d= n-1
    while(d%2==0):
        d//=2
        r+=1
    
    for i in range(k):
        a= random.randint(2,n-2)
        x = pow(a,d,n)
        if x==1 or x==n-1:
            continue
        for j in range(r-1):
            x= pow(x,2,n)
            if x==n-1:
                break
            else:
                return False
    return True


