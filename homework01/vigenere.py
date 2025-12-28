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
    # PUT YOUR CODE HERE

    keyword = keyword.lower()
    key_index = 0

    for ch in plaintext:
        if "a" <= ch <= "z":
            shift = ord(keyword[key_index % len(keyword)]) - ord("a")
            ciphertext += chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
            key_index += 1
        elif "A" <= ch <= "Z":
            shift = ord(keyword[key_index % len(keyword)]) - ord("a")
            ciphertext += chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
            key_index += 1
        else:
            ciphertext += ch

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
    # PUT YOUR CODE HERE

    keyword = keyword.lower()
    key_index = 0

    for ch in ciphertext:
        if "a" <= ch <= "z":
            shift = ord(keyword[key_index % len(keyword)]) - ord("a")
            plaintext += chr((ord(ch) - ord("a") - shift) % 26 + ord("a"))
            key_index += 1
        elif "A" <= ch <= "Z":
            shift = ord(keyword[key_index % len(keyword)]) - ord("a")
            plaintext += chr((ord(ch) - ord("A") - shift) % 26 + ord("A"))
            key_index += 1
        else:
            plaintext += ch

    return plaintext
