import random

primes = [19, 23, 29, 47, 59, 61, 97, 109, 113, 131, 149, 167, 179, 181, 193, 223, 229, 233, 257, 263]


# Legnagyobb közös osztó Euklideszi Algoritmus
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Inverz moduló
def imod(a, n):
    c = 1
    while c % a > 0:
        c += n
    return c // a  # floor osztás


# Euler's Totient Phi (realtiv primek szama)
def num_of_rel_primes(szam):
    i = 0
    for each in range(1, szam):
        if gcd(each, szam) == 1:
            i += 1
    return i


def generate_keypair():
    p, q = 1, 1

    while p == q:
        p = primes[random.randrange(len(primes))]
        q = primes[random.randrange(len(primes))]

    n = p * q

    # Relatív prímek száma
    phi = (p - 1) * (q - 1)

    # Euclideszi algoritmus: ramdom e and phi(n) relatív prím
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Kiegészitett Euclideszi Algoritmus a privát kulcsgeneráláshoz
    d = imod(e, phi)

    # Publikus (e, n) Privát (d, n)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    key, n = pk
    # a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # byte array
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    # a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # byte array to string
    return ''.join(plain)
