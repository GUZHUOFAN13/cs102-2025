def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    key_index = 0
    keyword = keyword.lower()

    for ch in plaintext:
        if 'a' <= ch <= 'z':
            shift = ord(keyword[key_index % len(keyword)]) - ord('a')
            ciphertext += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
            key_index += 1
        elif 'A' <= ch <= 'Z':
            shift = ord(keyword[key_index % len(keyword)]) - ord('a')
            ciphertext += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            key_index += 1
        else:
            ciphertext += ch

    return ciphertext



def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    key_index = 0
    keyword = keyword.lower()

    for ch in ciphertext:
        if 'a' <= ch <= 'z':
            shift = ord(keyword[key_index % len(keyword)]) - ord('a')
            plaintext += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
            key_index += 1
        elif 'A' <= ch <= 'Z':
            shift = ord(keyword[key_index % len(keyword)]) - ord('a')
            plaintext += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
            key_index += 1
        else:
            plaintext += ch

    return plaintext
