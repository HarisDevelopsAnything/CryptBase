def test_key(key):
    for i in range(2,26):
        if(key%i==0 and 26%i==0):
            return False
    return True

def mod_inv(key):
    for i in range(1,26):
        if(key*i%26 == 1):
            return i
    return -1

def affine_encrypt(text, key1, key2):
    """Encrypt text using affine cipher"""

    if not test_key(key1):
       raise ValueError("Key 1 must be coprime with 26!")
    
    res = ''
    for i in range(0,len(text)):
        x = ord(text[i])
        if x>=65 and x<=90:
            res+= chr((key1*(x-65)+key2)%26+65)
        elif x>=97 and x<=122:
            res+= chr((key1*(x-97)+key2)%26+97)
        else:
            res+= text[i]

    
    return {
        'encrypted': res
    }

def affine_decrypt(text, key1, key2):
    """Decrypt text using affine cipher"""
    
    if not test_key(key1):
       raise ValueError("Key 1 must be coprime with 26!")
    
    res = ''
    inv = mod_inv(key1)
    for i in range(0,len(text)):
        x = ord(text[i])
        if x>=65 and x<=90:
            nc = ord(text[i])-65
            res+= chr((nc-key2)*inv%26+65)
        elif x>=97 and x<=122:
            nc = ord(text[i])-97
            res+= chr((nc-key2)*inv%26+97)
        else:
            res+= text[i]

    
    return {
        'decrypted': res
    }