from math import ceil


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


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    if keyword == "":
        raise ValueError("Keyword could not be empty")
    ciphertext = ""
    # растянем ключ хотя бы до длины текста
    long_key = (keyword * ceil(len(plaintext) / len(keyword)))[: len(plaintext)]
    for i in range(len(plaintext)):
        ciphertext += shift_symbol(plaintext[i], ord(long_key[i].lower()) - 97)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    if keyword == "":
        raise ValueError("Keyword could not be empty")
    plaintext = ""
    long_key = (keyword * ceil(len(ciphertext) / len(keyword)))[: len(ciphertext)]
    for i in range(len(ciphertext)):
        plaintext += shift_symbol(ciphertext[i], -(ord(long_key[i].lower()) - 97))
    return plaintext
