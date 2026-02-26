from algorithms.gcd import gcd

def checkPrime(n):
    for i in range(n/2):
        if n%i==0:
            return False
    return True


def keygen(p,q):
    if not checkPrime(p) or not checkPrime(q):
        return -1
    phi = (p-1)*(q-1)
    n = p*q
    e=0
    d=0
    for e in range(2,phi):
        if gcd(e,phi)==1:
            break

    for d in range(1,e+1):
        if (d*e)%phi == 1:
            break
    
    return (e,d,n)

        
def rsa_encrypt(plain, p, q):
    e,_,n = keygen(p,q)
    return (plain**e)%n

def rsa_decrypt(cipher, p, q):
    _,d,n = keygen(p,q)
    return (cipher**d)%n