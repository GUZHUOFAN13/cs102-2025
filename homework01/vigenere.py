ALPHABET_SIZE = 26


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
    ciphertext = ""
    key_idx = 0
    key_len = len(keyword)
    for key_idx, ch in enumerate(plaintext):
        if "A" <= ch <= "Z":
            a_letter_index = ord("A")
        elif "a" <= ch <= "z":
            a_letter_index = ord("a")
        else:
            ciphertext += ch
            continue

        pos = ord(ch) - a_letter_index
        key_char = keyword[key_idx % key_len]
        shift = ord(key_char) - a_letter_index
        new_pos = pos + shift
        new_ch = chr(a_letter_index + new_pos % ALPHABET_SIZE)
        ciphertext += new_ch

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
    plaintext = ""
    key_len = len(keyword)
    key_idx = 0

    for key_idx, ch in enumerate(ciphertext):
        if "A" <= ch <= "Z":
            a_letter_index = ord("A")
        elif "a" <= ch <= "z":
            a_letter_index = ord("a")
        else:
            plaintext += ch
            continue

        pos = ord(ch) - a_letter_index
        key_let = keyword[key_idx % key_len]
        shift = ord(key_let) - a_letter_index
        new_pos = pos - shift
        new_ch = chr(a_letter_index + new_pos % ALPHABET_SIZE)
        plaintext += new_ch

    return plaintext
