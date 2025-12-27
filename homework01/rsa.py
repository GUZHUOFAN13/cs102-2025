import random
import typing as tp


def is_prime(n: int) -> bool:
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True


def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    d = 1
    while (d * e) % phi != 1:
        d += 1
    return d


def generate_keypair(
    p: int, q: int
) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = multiplicative_inverse(e, phi)

    return (e, n), (d, n)


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    key, n = pk
    return [(ord(char) ** key) % n for char in plaintext]


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    key, n = pk
    return "".join(chr((char ** key) % n) for char in ciphertext)


