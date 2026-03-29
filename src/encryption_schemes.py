import base64

def shift_cipher(char, key=3):
    """
    Encrypts a character using a shift cipher (Caesar cipher).
    Shifts the character's ASCII value by the key.
    """
    encrypted_char = chr(ord(char) + key)
    return encrypted_char

def xor_cipher(char, key=0x5A):
    """
    Encrypts a character using an XOR cipher.
    XORs the character's ASCII value with the key.
    """
    encrypted_char = chr(ord(char) ^ key)
    return encrypted_char

def substitution_cipher(char, key=None):
    """
    Encrypts a character using a simple substitution cipher.
    A fixed substitution map is used.
    """
    substitution_map = {
        'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v', 'f': 'u', 'g': 't', 'h': 's',
        'i': 'r', 'j': 'q', 'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l', 'p': 'k',
        'q': 'j', 'r': 'i', 's': 'h', 't': 'g', 'u': 'f', 'v': 'e', 'w': 'd', 'x': 'c',
        'y': 'b', 'z': 'a',
        'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T', 'H': 'S',
        'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K',
        'Q': 'J', 'R': 'I', 'S': 'H', 'T': 'G', 'U': 'F', 'V': 'E', 'W': 'D', 'X': 'C',
        'Y': 'B', 'Z': 'A',
    }
    return substitution_map.get(char, char)

def base64_encode(char, key=None):
    """
    "Encrypts" a character by Base64 encoding its byte representation.
    """
    encoded_bytes = base64.b64encode(char.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def reverse_bits(char, key=None):
    """
    "Encrypts" a character by reversing the bits of its ASCII value.
    """
    byte = ord(char)
    reversed_byte = int(f'{byte:08b}'[::-1], 2)
    return chr(reversed_byte)

# A dictionary to hold all the encryption schemes
ENCRYPTION_SCHEMES = {
    'shift': shift_cipher,
    'xor': xor_cipher,
    'substitution': substitution_cipher,
    'base64': base64_encode,
    'reverse_bits': reverse_bits,
}
