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
    for i in plaintext:
        new_letter = ord(i) + shift
        if ord("a") <= ord(i) <= ord("z"):
            if new_letter > ord("z"):
                new_letter = new_letter - 26
            i = chr(new_letter)
        if ord("A") <= ord(i) <= ord("Z"):
            if new_letter > ord("Z"):
                new_letter = new_letter - 26
            i = chr(new_letter)
        ciphertext = ciphertext + i

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
    for i in ciphertext:
        new_letter = ord(i) - shift
        if ord("a") <= ord(i) <= ord("z"):
            if new_letter < ord("a"):
                new_letter = new_letter + 26
            i = chr(new_letter)
        if ord("A") <= ord(i) <= ord("Z"):
            if new_letter < ord("A"):
                new_letter = new_letter + 26
            i = chr(new_letter)
        plaintext = plaintext + i

    return plaintext
