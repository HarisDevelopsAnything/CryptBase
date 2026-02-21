# AES-128 Implementation (no built-in crypto functions)
# Operates on 128-bit (16-byte) blocks with a 128-bit key
# 10 rounds of: SubBytes -> ShiftRows -> MixColumns -> AddRoundKey
# Final round omits MixColumns

# -------- S-Box (substitution lookup table) --------
S_BOX = [
    0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
    0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
    0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
    0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
    0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
    0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
    0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
    0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
    0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
    0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
    0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
    0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
    0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
    0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
    0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
    0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16,
]

# -------- Inverse S-Box (for decryption) --------
INV_S_BOX = [
    0x52,0x09,0x6A,0xD5,0x30,0x36,0xA5,0x38,0xBF,0x40,0xA3,0x9E,0x81,0xF3,0xD7,0xFB,
    0x7C,0xE3,0x39,0x82,0x9B,0x2F,0xFF,0x87,0x34,0x8E,0x43,0x44,0xC4,0xDE,0xE9,0xCB,
    0x54,0x7B,0x94,0x32,0xA6,0xC2,0x23,0x3D,0xEE,0x4C,0x95,0x0B,0x42,0xFA,0xC3,0x4E,
    0x08,0x2E,0xA1,0x66,0x28,0xD9,0x24,0xB2,0x76,0x5B,0xA2,0x49,0x6D,0x8B,0xD1,0x25,
    0x72,0xF8,0xF6,0x64,0x86,0x68,0x98,0x16,0xD4,0xA4,0x5C,0xCC,0x5D,0x65,0xB6,0x92,
    0x6C,0x70,0x48,0x50,0xFD,0xED,0xB9,0xDA,0x5E,0x15,0x46,0x57,0xA7,0x8D,0x9D,0x84,
    0x90,0xD8,0xAB,0x00,0x8C,0xBC,0xD3,0x0A,0xF7,0xE4,0x58,0x05,0xB8,0xB3,0x45,0x06,
    0xD0,0x2C,0x1E,0x8F,0xCA,0x3F,0x0F,0x02,0xC1,0xAF,0xBD,0x03,0x01,0x13,0x8A,0x6B,
    0x3A,0x91,0x11,0x41,0x4F,0x67,0xDC,0xEA,0x97,0xF2,0xCF,0xCE,0xF0,0xB4,0xE6,0x73,
    0x96,0xAC,0x74,0x22,0xE7,0xAD,0x35,0x85,0xE2,0xF9,0x37,0xE8,0x1C,0x75,0xDF,0x6E,
    0x47,0xF1,0x1A,0x71,0x1D,0x29,0xC5,0x89,0x6F,0xB7,0x62,0x0E,0xAA,0x18,0xBE,0x1B,
    0xFC,0x56,0x3E,0x4B,0xC6,0xD2,0x79,0x20,0x9A,0xDB,0xC0,0xFE,0x78,0xCD,0x5A,0xF4,
    0x1F,0xDD,0xA8,0x33,0x88,0x07,0xC7,0x31,0xB1,0x12,0x10,0x59,0x27,0x80,0xEC,0x5F,
    0x60,0x51,0x7F,0xA9,0x19,0xB5,0x4A,0x0D,0x2D,0xE5,0x7A,0x9F,0x93,0xC9,0x9C,0xEF,
    0xA0,0xE0,0x3B,0x4D,0xAE,0x2A,0xF5,0xB0,0xC8,0xEB,0xBB,0x3C,0x83,0x53,0x99,0x61,
    0x17,0x2B,0x04,0x7E,0xBA,0x77,0xD6,0x26,0xE1,0x69,0x14,0x63,0x55,0x21,0x0C,0x7D,
]

# -------- Round constants for key expansion --------
RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]


# ======== Helper / conversion functions ========

def hex_to_bytes(hex_str):
    """Convert a hex string like '00112233...' to a list of ints"""
    hex_str = hex_str.replace(' ', '')
    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string must have even length")
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]


def bytes_to_hex(byte_list):
    """Convert a list of ints to a hex string"""
    return ''.join(format(b, '02X') for b in byte_list)


def bytes_to_state(byte_list):
    """Convert 16 bytes into a 4x4 state matrix (column-major order).
    state[row][col] — AES fills columns first:
    byte0->s[0][0], byte1->s[1][0], byte2->s[2][0], byte3->s[3][0],
    byte4->s[0][1], ...
    """
    state = [[0]*4 for _ in range(4)]
    for i in range(16):
        state[i % 4][i // 4] = byte_list[i]
    return state


def state_to_bytes(state):
    """Convert 4x4 state matrix back to 16 bytes (column-major)"""
    result = []
    for col in range(4):
        for row in range(4):
            result.append(state[row][col])
    return result


def state_to_hex(state):
    """Pretty-print a state matrix as a hex string"""
    return bytes_to_hex(state_to_bytes(state))


def format_state_matrix(state):
    """Format state matrix as a list of row strings for display"""
    rows = []
    for row in range(4):
        rows.append(' '.join(format(state[row][col], '02X') for col in range(4)))
    return rows


# ======== AES Core Operations ========

def sub_bytes(state):
    """Replace each byte in the state with its S-Box value"""
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = S_BOX[state[r][c]]
    return result


def inv_sub_bytes(state):
    """Replace each byte with its Inverse S-Box value (decryption)"""
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = INV_S_BOX[state[r][c]]
    return result


def shift_rows(state):
    """Shift row i left by i positions:
    Row 0: no shift
    Row 1: shift left by 1
    Row 2: shift left by 2
    Row 3: shift left by 3
    """
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = state[r][(c + r) % 4]
    return result


def inv_shift_rows(state):
    """Shift row i right by i positions (decryption)"""
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = state[r][(c - r) % 4]
    return result


def xtime(a):
    """Multiply by 2 in GF(2^8): left-shift by 1, XOR with 0x1B if overflow"""
    result = (a << 1) & 0xFF
    if a & 0x80:  # if the high bit was set before shifting
        result ^= 0x1B
    return result


def gf_mul(a, b):
    """Multiply two bytes in GF(2^8) using repeated xtime.
    Decomposes b into powers of 2 and accumulates.
    """
    result = 0
    temp = a
    for i in range(8):
        if b & 1:
            result ^= temp
        temp = xtime(temp)
        b >>= 1
    return result


def mix_columns(state):
    """Mix each column using the fixed matrix:
    [2, 3, 1, 1]
    [1, 2, 3, 1]
    [1, 1, 2, 3]
    [3, 1, 1, 2]
    Each element = GF(2^8) multiply-and-XOR
    """
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        result[0][c] = gf_mul(col[0], 2) ^ gf_mul(col[1], 3) ^ col[2] ^ col[3]
        result[1][c] = col[0] ^ gf_mul(col[1], 2) ^ gf_mul(col[2], 3) ^ col[3]
        result[2][c] = col[0] ^ col[1] ^ gf_mul(col[2], 2) ^ gf_mul(col[3], 3)
        result[3][c] = gf_mul(col[0], 3) ^ col[1] ^ col[2] ^ gf_mul(col[3], 2)
    return result


def inv_mix_columns(state):
    """Inverse MixColumns using the inverse matrix:
    [14, 11, 13,  9]
    [ 9, 14, 11, 13]
    [13,  9, 14, 11]
    [11, 13,  9, 14]
    """
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        result[0][c] = gf_mul(col[0],14) ^ gf_mul(col[1],11) ^ gf_mul(col[2],13) ^ gf_mul(col[3], 9)
        result[1][c] = gf_mul(col[0], 9) ^ gf_mul(col[1],14) ^ gf_mul(col[2],11) ^ gf_mul(col[3],13)
        result[2][c] = gf_mul(col[0],13) ^ gf_mul(col[1], 9) ^ gf_mul(col[2],14) ^ gf_mul(col[3],11)
        result[3][c] = gf_mul(col[0],11) ^ gf_mul(col[1],13) ^ gf_mul(col[2], 9) ^ gf_mul(col[3],14)
    return result


def add_round_key(state, round_key):
    """XOR each byte of the state with the corresponding round key byte"""
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = state[r][c] ^ round_key[r][c]
    return result


# ======== Key Expansion ========

def rot_word(word):
    """Rotate a 4-byte word left by 1: [a,b,c,d] -> [b,c,d,a]"""
    return word[1:] + [word[0]]


def sub_word(word):
    """Apply S-Box to each byte in a 4-byte word"""
    return [S_BOX[b] for b in word]


def key_expansion(key_bytes):
    """Expand the 16-byte key into 11 round keys (44 words of 4 bytes each).
    Returns a list of 11 state matrices (4x4), one per round.
    Also returns detailed steps.
    """
    # The key schedule produces 44 words (w[0]..w[43])
    w = []
    key_steps = []

    # First 4 words come directly from the key
    for i in range(4):
        word = key_bytes[4*i : 4*i+4]
        w.append(word)

    key_steps.append({
        'description': 'Original key words',
        'words': [bytes_to_hex(w[i]) for i in range(4)]
    })

    # Generate remaining 40 words
    for i in range(4, 44):
        temp = list(w[i-1])  # copy
        step_detail = {'i': i}

        if i % 4 == 0:
            round_num = i // 4
            before_rot = bytes_to_hex(temp)
            temp = rot_word(temp)
            after_rot = bytes_to_hex(temp)
            temp = sub_word(temp)
            after_sub = bytes_to_hex(temp)
            rcon_val = RCON[round_num - 1]
            temp[0] ^= rcon_val
            after_rcon = bytes_to_hex(temp)

            step_detail['round'] = round_num
            step_detail['rotWord'] = f"{before_rot} → {after_rot}"
            step_detail['subWord'] = after_sub
            step_detail['rcon'] = format(rcon_val, '02X') + '000000'
            step_detail['afterRcon'] = after_rcon

        new_word = [w[i-4][j] ^ temp[j] for j in range(4)]
        step_detail['xor'] = f"w[{i-4}] ⊕ temp = {bytes_to_hex(new_word)}"
        w.append(new_word)

        if i % 4 == 0:
            key_steps.append(step_detail)

    # Convert 44 words into 11 round keys (each is a 4x4 state matrix)
    round_keys = []
    for rk in range(11):
        key_state = [[0]*4 for _ in range(4)]
        for c in range(4):
            word = w[rk*4 + c]
            for r in range(4):
                key_state[r][c] = word[r]
        round_keys.append(key_state)

    return round_keys, key_steps


# ======== Encrypt / Decrypt with full step tracking ========

def aes_encrypt(plaintext_hex, key_hex):
    """
    Encrypt 128-bit plaintext with 128-bit key using AES-128.
    Input: hex strings (32 hex chars each = 16 bytes).
    Returns encrypted hex and detailed steps.
    """
    pt_bytes = hex_to_bytes(plaintext_hex)
    key_bytes = hex_to_bytes(key_hex)

    if len(pt_bytes) != 16:
        raise ValueError("Plaintext must be exactly 16 bytes (32 hex characters)")
    if len(key_bytes) != 16:
        raise ValueError("Key must be exactly 16 bytes (32 hex characters)")

    # Key expansion
    round_keys, key_steps = key_expansion(key_bytes)

    state = bytes_to_state(pt_bytes)
    rounds = []

    # Record initial state
    rounds.append({
        'round': 0,
        'operation': 'Initial',
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    # Initial round: AddRoundKey
    state = add_round_key(state, round_keys[0])
    rounds.append({
        'round': 0,
        'operation': 'AddRoundKey',
        'roundKey': state_to_hex(round_keys[0]),
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    # Rounds 1 through 9
    for rnd in range(1, 10):
        round_detail = {'round': rnd, 'steps': []}

        # SubBytes
        state = sub_bytes(state)
        round_detail['steps'].append({
            'operation': 'SubBytes',
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        # ShiftRows
        state = shift_rows(state)
        round_detail['steps'].append({
            'operation': 'ShiftRows',
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        # MixColumns
        state = mix_columns(state)
        round_detail['steps'].append({
            'operation': 'MixColumns',
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        # AddRoundKey
        state = add_round_key(state, round_keys[rnd])
        round_detail['steps'].append({
            'operation': 'AddRoundKey',
            'roundKey': state_to_hex(round_keys[rnd]),
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        rounds.append(round_detail)

    # Final round (10): SubBytes, ShiftRows, AddRoundKey (no MixColumns)
    final_detail = {'round': 10, 'steps': []}

    state = sub_bytes(state)
    final_detail['steps'].append({
        'operation': 'SubBytes',
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    state = shift_rows(state)
    final_detail['steps'].append({
        'operation': 'ShiftRows',
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    state = add_round_key(state, round_keys[10])
    final_detail['steps'].append({
        'operation': 'AddRoundKey',
        'roundKey': state_to_hex(round_keys[10]),
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    rounds.append(final_detail)

    ciphertext = state_to_hex(state)

    return {
        'encrypted': ciphertext,
        'steps': {
            'keyExpansion': key_steps,
            'roundKeys': [state_to_hex(rk) for rk in round_keys],
            'rounds': rounds,
        }
    }


def aes_decrypt(ciphertext_hex, key_hex):
    """
    Decrypt 128-bit ciphertext with 128-bit key using AES-128.
    Inverse operations in reverse order.
    """
    ct_bytes = hex_to_bytes(ciphertext_hex)
    key_bytes = hex_to_bytes(key_hex)

    if len(ct_bytes) != 16:
        raise ValueError("Ciphertext must be exactly 16 bytes (32 hex characters)")
    if len(key_bytes) != 16:
        raise ValueError("Key must be exactly 16 bytes (32 hex characters)")

    # Key expansion (same as encryption)
    round_keys, key_steps = key_expansion(key_bytes)

    state = bytes_to_state(ct_bytes)
    rounds = []

    # Record initial state
    rounds.append({
        'round': 0,
        'operation': 'Initial Ciphertext',
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    # Initial round: AddRoundKey with last round key (key 10)
    state = add_round_key(state, round_keys[10])
    rounds.append({
        'round': 0,
        'operation': 'AddRoundKey (Key 10)',
        'roundKey': state_to_hex(round_keys[10]),
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    # Rounds 9 down to 1
    for rnd in range(9, 0, -1):
        round_detail = {'round': 10 - rnd, 'actualKeyRound': rnd, 'steps': []}

        # InvShiftRows
        state = inv_shift_rows(state)
        round_detail['steps'].append({
            'operation': 'InvShiftRows',
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        # InvSubBytes
        state = inv_sub_bytes(state)
        round_detail['steps'].append({
            'operation': 'InvSubBytes',
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        # AddRoundKey
        state = add_round_key(state, round_keys[rnd])
        round_detail['steps'].append({
            'operation': f'AddRoundKey (Key {rnd})',
            'roundKey': state_to_hex(round_keys[rnd]),
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        # InvMixColumns
        state = inv_mix_columns(state)
        round_detail['steps'].append({
            'operation': 'InvMixColumns',
            'state': format_state_matrix(state),
            'stateHex': state_to_hex(state),
        })

        rounds.append(round_detail)

    # Final round: InvShiftRows, InvSubBytes, AddRoundKey (key 0)
    final_detail = {'round': 10, 'actualKeyRound': 0, 'steps': []}

    state = inv_shift_rows(state)
    final_detail['steps'].append({
        'operation': 'InvShiftRows',
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    state = inv_sub_bytes(state)
    final_detail['steps'].append({
        'operation': 'InvSubBytes',
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    state = add_round_key(state, round_keys[0])
    final_detail['steps'].append({
        'operation': 'AddRoundKey (Key 0)',
        'roundKey': state_to_hex(round_keys[0]),
        'state': format_state_matrix(state),
        'stateHex': state_to_hex(state),
    })

    rounds.append(final_detail)

    plaintext = state_to_hex(state)

    return {
        'decrypted': plaintext,
        'steps': {
            'keyExpansion': key_steps,
            'roundKeys': [state_to_hex(rk) for rk in round_keys],
            'rounds': rounds,
        }
    }
