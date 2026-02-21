def vigenere_encrypt(text, key):
    """Encrypt text using vigenere cipher"""
    
    res = ''
    for i in range(0,len(text)):
        x = ord(text[i])
        shift = ord(key.upper()[i%len(key)])-65
        if x>=65 and x<=90:
            res+= chr((x-65+shift)%26+65)
        elif x>=97 and x<=122:
            res+= chr((x-97+shift)%26+97)
        else:
            res+= text[i]

    
    return {
        'encrypted': res
    }
def vigenere_decrypt(text, key):
    """Decrypt text using vigenere cipher"""
    
    res = ''
    for i in range(0,len(text)):
        x = ord(text[i])
        shift = ord(key.upper()[i%len(key)])-65
        if x>=65 and x<=90:
            res+= chr((x-65-shift)%26+65)
        elif x>=97 and x<=122:
            res+= chr((x-97-shift)%26+97)
        else:
            res+= text[i]

    
    return {
        'decrypted': res
    }