"""Module for decoding and encoding Caesar cipher"""


def shift_symbol(symbol: str, shift: int) -> str:
    """Shift a single alphabetic symbol by `shift` preserving case.
    Non-letters are returned unchanged.
    """
    code = ord(symbol)
    if 97 <= code <= 122:  # 'a'..'z'
        return chr((code + shift - 97) % 26 + 97)
    if 65 <= code <= 90:  # 'A'..'Z'
        return chr((code + shift - 65) % 26 + 65)
    return symbol


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for symbol in plaintext:
        ciphertext += shift_symbol(symbol, shift)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for symbol in ciphertext:
        plaintext += shift_symbol(symbol, -shift)
    return plaintext
