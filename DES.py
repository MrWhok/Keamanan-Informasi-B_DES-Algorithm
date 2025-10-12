
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

KEY_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]



def permute(block, table):
    return [block[i - 1] for i in table]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def string_to_bits(text):
    bits = []
    for char in text:
        bin_val = format(ord(char), '08b')
        bits.extend([int(b) for b in bin_val])
    return bits

def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        byte_str = ''.join(map(str, byte_bits))
        char_code = int(byte_str, 2)
        chars.append(chr(char_code))
    return "".join(chars)

def bits_to_hex(bits):
    hex_chars = []
    for i in range(0, len(bits), 4):
        nibble_bits = bits[i:i+4]
        nibble_str = ''.join(map(str, nibble_bits))
        hex_val = hex(int(nibble_str, 2))[2:] # remove '0x'
        hex_chars.append(hex_val)
    return "".join(hex_chars)



def generate_round_keys(key_bits):
    key_56 = permute(key_bits, PC1)

    left_half = key_56[:28]
    right_half = key_56[28:]

    round_keys = []
    for i in range(16):
        shift = KEY_SHIFTS[i]
        left_half = left_half[shift:] + left_half[:shift]
        right_half = right_half[shift:] + right_half[:shift]

        # 48 Bits
        combined_key = left_half + right_half
        round_key = permute(combined_key, PC2)
        round_keys.append(round_key)

    return round_keys



def mangler_function(right_half, round_key):
    expanded_bits = permute(right_half, E)

    xored_bits = xor(expanded_bits, round_key)

    s_box_output = []
    for i in range(8):
        chunk = xored_bits[i*6 : (i+1)*6]
        
        row = int(str(chunk[0]) + str(chunk[5]), 2)
        col = int("".join(map(str, chunk[1:5])), 2)
        
        val = S_BOXES[i][row][col]
        s_box_output.extend([int(b) for b in format(val, '04b')])
    
    p_box_output = permute(s_box_output, P)
    
    return p_box_output



def des_process(block_bits, key_bits, mode='encrypt'):

    round_keys = generate_round_keys(key_bits)
    if mode == 'decrypt':
        round_keys.reverse()

    permuted_block = permute(block_bits, IP)
    
    left_half = permuted_block[:32]
    right_half = permuted_block[32:]

    for i in range(16):
        f_result = mangler_function(right_half, round_keys[i])
        
        new_right_half = xor(left_half, f_result)
        
        new_left_half = right_half
        
        left_half, right_half = new_left_half, new_right_half

    final_block = right_half + left_half
    
    processed_block = permute(final_block, FP)
    
    return processed_block

def pad(text):
    pad_len = 8 - (len(text) % 8)
    padding = chr(pad_len) * pad_len
    return text + padding

def unpad(text):
    pad_len = ord(text[-1])
    return text[:-pad_len]

def des_encrypt(plaintext, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 characters (64 bits) long.")
    
    padded_text = pad(plaintext)
    key_bits = string_to_bits(key)
    ciphertext_bits = []
    
    for i in range(0, len(padded_text), 8):
        block = padded_text[i:i+8]
        block_bits = string_to_bits(block)
        encrypted_block = des_process(block_bits, key_bits, mode='encrypt')
        ciphertext_bits.extend(encrypted_block)
        
    return ciphertext_bits

def des_decrypt(ciphertext_bits, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 characters (64 bits) long.")
        
    key_bits = string_to_bits(key)
    decrypted_text_bits = []
    
    for i in range(0, len(ciphertext_bits), 64):
        block_bits = ciphertext_bits[i:i+64]
        decrypted_block = des_process(block_bits, key_bits, mode='decrypt')
        decrypted_text_bits.extend(decrypted_block)
        
    decrypted_text = bits_to_string(decrypted_text_bits)
    return unpad(decrypted_text)



if __name__ == "__main__":

    plaintext = input("Enter the text to encrypt: ")

    key = ""
    while len(key) != 8:
        key = input("Enter your 8-character secret key: ")
        if len(key) != 8:
            print("Error: The key must be exactly 8 characters long. Please try again.")

    print(f"Original Plaintext: '{plaintext}'")
    print(f"Key: '{key}'\n")

    encrypted_bits = des_encrypt(plaintext, key)
    encrypted_hex = bits_to_hex(encrypted_bits)
    print(f"Encrypted (Hex): {encrypted_hex}")

    decrypted_text = des_decrypt(encrypted_bits, key)
    print(f"Decrypted Text: '{decrypted_text}'\n")
    
    if plaintext == decrypted_text:
        print("Verification successfu.")
    else:
        print("Verification failed.")
