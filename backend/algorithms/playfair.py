def rowcol(keymat, c):
    for i in range(5):
        for j in range(5):
            if(keymat[i][j]==c):
                rc = [i,j]
                return rc
    return []

def create_key_matrix(key_input):
    """Create 5x5 key matrix from the given key"""
    key= []
    
    i=0
    while i<len(key_input):
        if key_input[i] not in key:
            key.append(key_input[i])
        i+=1
    for i in range(65,91):
        if chr(i) not in key and chr(i)!='J':
            key.append(chr(i))
    
    keymat = []
    for i in range(5):
        l = []
        for j in range(5):
            l.append(key[i*5+j])
        keymat.append(l)
    
    return keymat

def create_digraphs(text):
    """Split text into digraphs"""
    text = text.upper()
    text = text.replace('J', 'I')
    
    digraph = []
    if(len(text)%2!=0):
        text+='Z'
    
    start=0
    while(start<=len(text)-2):
        curr=''
        if(text[start]==text[start+1]):
            curr+= text[start]+'X'
            start+=1
        else:
            curr+= text[start]+text[start+1]
            start+=2
        digraph.append(curr)
    
    return digraph

def playfair_encrypt(text, key_input):
    """Encrypt text using Playfair cipher"""
    keymat = create_key_matrix(key_input)
    digraph = create_digraphs(text)
    
    res = ''
    for pair in digraph:
        rowcol1 = rowcol(keymat,pair[0])
        rowcol2 = rowcol(keymat,pair[1])
        if(rowcol1[0] == rowcol2[0]):
            res+=(keymat[rowcol1[0]][(rowcol1[1]+1)%5]+keymat[rowcol2[0]][(rowcol2[1]+1)%5])
        elif(rowcol1[1] == rowcol2[1]):
            res+=(keymat[(rowcol1[0]+1)%5][rowcol1[1]]+keymat[(rowcol2[0]+1)%5][rowcol2[1]])
        else:
            res+=(keymat[rowcol1[0]][rowcol2[1]]+keymat[rowcol2[0]][rowcol1[1]])
    
    return {
        'encrypted': res,
        'keyMatrix': keymat,
        'digraphs': digraph
    }

def playfair_decrypt(text, key_input):
    """Decrypt text using Playfair cipher"""
    keymat = create_key_matrix(key_input)
    digraph = create_digraphs(text)
    
    res = ''
    for pair in digraph:
        rowcol1 = rowcol(keymat,pair[0])
        rowcol2 = rowcol(keymat,pair[1])
        if(rowcol1[0] == rowcol2[0]):
            col1 = (rowcol1[1]-1)%5
            col2 = (rowcol2[1]-1)%5
            col1 = col1+5 if col1 < 0 else col1
            col2 = col2+5 if col2 < 0 else col2
            res+=(keymat[rowcol1[0]][col1]+keymat[rowcol2[0]][col2])
        elif(rowcol1[1] == rowcol2[1]):
            row1 = (rowcol1[0]-1)%5
            row2 = (rowcol2[0]-1)%5
            row1 = row1+5 if row1 < 0 else row1
            row2 = row2+5 if row2 < 0 else row2
            res+=(keymat[row1][rowcol1[1]]+keymat[row2][rowcol2[1]])
        else:
            res+=(keymat[rowcol1[0]][rowcol2[1]]+keymat[rowcol2[0]][rowcol1[1]])
    
    return {
        'decrypted': res,
        'keyMatrix': keymat,
        'digraphs': digraph
    }