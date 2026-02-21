def gcd_with_steps(a, b):
    """
    Calculate GCD using Euclidean algorithm with detailed steps
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        dict: Contains gcd value and steps list
    """
    steps = []
    original_a, original_b = a, b
    
    # Ensure a >= b for consistency
    if a < b:
        a, b = b, a
        steps.append({
            'step': 1,
            'description': f'Swap numbers to ensure a ≥ b',
            'calculation': f'a = {a}, b = {b}',
            'result': f'Start with larger number first'
        })
    else:
        steps.append({
            'step': 1,
            'description': f'Initial values',
            'calculation': f'a = {a}, b = {b}',
            'result': f'Find GCD of {a} and {b}'
        })
    
    step_num = 2
    
    # Euclidean algorithm with steps
    while b != 0:
        quotient = a // b
        remainder = a % b
        
        steps.append({
            'step': step_num,
            'description': f'Apply Euclidean algorithm',
            'calculation': f'{a} = {b} × {quotient} + {remainder}',
            'result': f'remainder = {remainder}'
        })
        
        a, b = b, remainder
        step_num += 1
    
    # Final result
    steps.append({
        'step': step_num,
        'description': 'Conclusion',
        'calculation': f'Remainder is 0',
        'result': f'GCD({original_a}, {original_b}) = {a}'
    })
    
    return {
        'gcd': a,
        'steps': steps
    }

def gcd(a,b):
    if a>b:
        return euc(a,b)
    else:
        return euc(b,a)

def euc(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a % b)