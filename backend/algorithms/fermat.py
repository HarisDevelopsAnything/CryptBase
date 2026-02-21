import random

def fermat_test(n, k):
    """
    Fermat's primality test with steps
    
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
    
    steps.append({
        'step': 1,
        'description': f'Testing n = {n} with {k} iterations',
        'result': f'n-1 = {n-1}'
    })
    
    # Step 2-k+1: Test k random witnesses
    for i in range(k):
        a = random.randint(2, n - 2)
        
        # Calculate a^(n-1) mod n
        result = pow(a, n - 1, n)
        
        step_num = i + 2
        if result == 1:
            steps.append({
                'step': step_num,
                'description': f'Iteration {i+1}: Testing with a = {a}',
                'calculation': f'{a}^{n-1} mod {n} = {result}',
                'result': f'✓ Passed (result = 1, consistent with Fermat\'s Little Theorem)'
            })
        else:
            steps.append({
                'step': step_num,
                'description': f'Iteration {i+1}: Testing with a = {a}',
                'calculation': f'{a}^{n-1} mod {n} = {result}',
                'result': f'✗ Failed (result ≠ 1, {n} is composite)'
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
        'result': f'All {k} iterations passed. {n} is probably prime with high probability'
    })
    
    return {'isPrime': True, 'steps': steps}
