def p10(key, p):
    """Apply P10 permutation to 10-bit key"""
    if len(key) != 10 or len(p) != 10:
        raise ValueError('P-10 failed, invalid key or permutation length')
    l = []
    for temp in p:
        if temp > 10 or temp < 1:
            raise ValueError("P-10 failed, invalid permutation value")
        l.append(key[temp - 1])
    return l


def ls1(key):
    """Left shift each 5-bit half by 1 position"""
    if len(key) != 10:
        raise ValueError("Invalid key length!")
    left = key[:5]
    right = key[5:]
    left = left[1:] + [left[0]]
    right = right[1:] + [right[0]]
    return left + right


def ls2(key):
    """Left shift each 5-bit half by 2 positions"""
    if len(key) != 10:
        raise ValueError("Invalid key length!")
    left = key[:5]
    right = key[5:]
    left = left[2:] + left[:2]
    right = right[2:] + right[:2]
    return left + right


def p8(key, p):
    """Apply P8 permutation to extract 8-bit subkey from 10-bit key"""
    if len(key) != 10 or len(p) != 8:
        raise ValueError("P-8 failed, invalid lengths")
    l = []
    for temp in p:
        if temp > 10 or temp < 1:
            raise ValueError("P-8 failed, invalid permutation value")
        l.append(key[temp - 1])
    return l


def p4(bits, p):
    """Apply P4 permutation to 4-bit input"""
    if len(bits) != 4 or len(p) != 4:
        raise ValueError("P-4 failed, invalid lengths")
    l = []
    for temp in p:
        if temp > 4 or temp < 1:
            raise ValueError("P-4 failed, invalid permutation value")
        l.append(bits[temp - 1])
    return l


def ip(pt, ipv):
    """Apply initial permutation to 8-bit input"""
    if len(pt) != 8 or len(ipv) != 8:
        raise ValueError("IP failed, invalid plaintext or permutation length")
    l = []
    for temp in ipv:
        if temp < 1 or temp > 8:
            raise ValueError("IP failed, invalid permutation value")
        l.append(pt[temp - 1])
    return l


def ep(right_half, epv):
    """Apply expansion permutation: expand 4 bits to 8 bits"""
    if len(right_half) != 4 or len(epv) != 8:
        raise ValueError("EP failed, invalid lengths")
    l = []
    for temp in epv:
        if temp < 1 or temp > 4:
            raise ValueError("EP failed, invalid permutation value")
        l.append(right_half[temp - 1])
    return l


def xor(b1, b2):
    """XOR two binary lists"""
    if len(b1) != len(b2):
        raise ValueError('Non matching binary lengths')
    l = []
    for i in range(len(b1)):
        l.append(0 if b1[i] == b2[i] else 1)
    return l


def binToDec(b0, b1):
    """Convert 2 bits to decimal"""
    return b0 * 2 + b1


def intToBin2(n):
    """Convert integer (0-3) to 2-bit binary list"""
    return [n >> 1 & 1, n & 1]


def sbox_lookup(bits, s_table):
    """Look up value in S-box. Row = bit0,bit3; Col = bit1,bit2"""
    row = binToDec(bits[0], bits[3])
    col = binToDec(bits[1], bits[2])
    return intToBin2(s_table[row][col])


def sbox(expanded, subkey, s0, s1):
    """Apply S-box substitution after XOR with subkey"""
    xored = xor(expanded, subkey)
    left = xored[:4]
    right = xored[4:]
    s0_result = sbox_lookup(left, s0)
    s1_result = sbox_lookup(right, s1)
    return s0_result + s1_result


def fk(bits, subkey, epv, s0, s1, p4v):
    """The complex function fk used in S-DES"""
    left = bits[:4]
    right = bits[4:]

    # Expansion/permutation on right half
    expanded = ep(right, epv)

    # S-box substitution (includes XOR with subkey)
    sbox_output = sbox(expanded, subkey, s0, s1)

    # P4 permutation
    p4_result = p4(sbox_output, p4v)

    # XOR with left half
    new_left = xor(left, p4_result)

    return new_left + right


def sw(bits):
    """Swap left and right halves"""
    return bits[4:] + bits[:4]


def generate_keys(key, p10v, p8v):
    """Generate K1 and K2 from 10-bit key"""
    p10_result = p10(key, p10v)
    ls1_result = ls1(p10_result)
    k1 = p8(ls1_result, p8v)
    ls2_result = ls2(ls1_result)
    k2 = p8(ls2_result, p8v)
    return k1, k2


def str_to_bits(s):
    """Convert a string of 0s and 1s to a list of ints"""
    return [int(c) for c in s if c in ('0', '1')]


def bits_to_str(bits):
    """Convert a list of int bits to a string"""
    return ''.join(str(b) for b in bits)


def parse_int_list(s):
    """Parse a space or comma separated string into a list of ints"""
    return [int(x) for x in s.replace(',', ' ').split()]


def parse_sbox(s):
    """Parse a flat list of 16 values into a 4x4 S-box matrix"""
    flat = parse_int_list(s)
    if len(flat) != 16:
        raise ValueError("S-box must have exactly 16 values (4x4 matrix)")
    return [flat[i * 4:(i + 1) * 4] for i in range(4)]


def des_encrypt(plaintext, key, p10v, p8v, ipv, ipinv, epv, p4v, s0, s1):
    """
    Encrypt 8-bit plaintext using S-DES.
    plaintext: 8-bit binary string (e.g. '10010111')
    key: 10-bit binary string (e.g. '1010000010')
    Other params: space/comma separated permutation values and S-box values.
    """
    pt_bits = str_to_bits(plaintext)
    key_bits = str_to_bits(key)

    if len(pt_bits) != 8:
        raise ValueError("Plaintext must be exactly 8 bits")
    if len(key_bits) != 10:
        raise ValueError("Key must be exactly 10 bits")

    p10_perm = parse_int_list(p10v)
    p8_perm = parse_int_list(p8v)
    ip_perm = parse_int_list(ipv)
    ip_inv_perm = parse_int_list(ipinv)
    ep_perm = parse_int_list(epv)
    p4_perm = parse_int_list(p4v)
    s0_matrix = parse_sbox(s0)
    s1_matrix = parse_sbox(s1)

    # Key generation
    k1, k2 = generate_keys(key_bits, p10_perm, p8_perm)

    steps = {}
    steps['plaintext'] = bits_to_str(pt_bits)
    steps['key'] = bits_to_str(key_bits)

    p10_result = p10(key_bits, p10_perm)
    steps['p10'] = bits_to_str(p10_result)

    ls1_result = ls1(p10_result)
    steps['ls1'] = bits_to_str(ls1_result)
    steps['k1'] = bits_to_str(k1)

    ls2_result = ls2(ls1_result)
    steps['ls2'] = bits_to_str(ls2_result)
    steps['k2'] = bits_to_str(k2)

    # Encryption rounds
    ip_result = ip(pt_bits, ip_perm)
    steps['ip'] = bits_to_str(ip_result)

    fk1_result = fk(ip_result, k1, ep_perm, s0_matrix, s1_matrix, p4_perm)
    steps['fk1'] = bits_to_str(fk1_result)

    sw_result = sw(fk1_result)
    steps['sw'] = bits_to_str(sw_result)

    fk2_result = fk(sw_result, k2, ep_perm, s0_matrix, s1_matrix, p4_perm)
    steps['fk2'] = bits_to_str(fk2_result)

    ciphertext = ip(fk2_result, ip_inv_perm)
    steps['ciphertext'] = bits_to_str(ciphertext)

    return {
        'encrypted': bits_to_str(ciphertext),
        'steps': steps
    }


def des_decrypt(ciphertext, key, p10v, p8v, ipv, ipinv, epv, p4v, s0, s1):
    """
    Decrypt 8-bit ciphertext using S-DES.
    Same as encryption but with keys applied in reverse order (K2 first, then K1).
    """
    ct_bits = str_to_bits(ciphertext)
    key_bits = str_to_bits(key)

    if len(ct_bits) != 8:
        raise ValueError("Ciphertext must be exactly 8 bits")
    if len(key_bits) != 10:
        raise ValueError("Key must be exactly 10 bits")

    p10_perm = parse_int_list(p10v)
    p8_perm = parse_int_list(p8v)
    ip_perm = parse_int_list(ipv)
    ip_inv_perm = parse_int_list(ipinv)
    ep_perm = parse_int_list(epv)
    p4_perm = parse_int_list(p4v)
    s0_matrix = parse_sbox(s0)
    s1_matrix = parse_sbox(s1)

    # Key generation
    k1, k2 = generate_keys(key_bits, p10_perm, p8_perm)

    steps = {}
    steps['ciphertext'] = bits_to_str(ct_bits)
    steps['key'] = bits_to_str(key_bits)
    steps['k1'] = bits_to_str(k1)
    steps['k2'] = bits_to_str(k2)

    # Decryption rounds (keys reversed: K2 first, then K1)
    ip_result = ip(ct_bits, ip_perm)
    steps['ip'] = bits_to_str(ip_result)

    fk1_result = fk(ip_result, k2, ep_perm, s0_matrix, s1_matrix, p4_perm)
    steps['fk1'] = bits_to_str(fk1_result)

    sw_result = sw(fk1_result)
    steps['sw'] = bits_to_str(sw_result)

    fk2_result = fk(sw_result, k1, ep_perm, s0_matrix, s1_matrix, p4_perm)
    steps['fk2'] = bits_to_str(fk2_result)

    plaintext = ip(fk2_result, ip_inv_perm)
    steps['plaintext'] = bits_to_str(plaintext)

    return {
        'decrypted': bits_to_str(plaintext),
        'steps': steps
    }

