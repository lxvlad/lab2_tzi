"""
Завдання 1. Потоковий шифр на основі генератора BBS 
1. Створити програму, яка реалізовує потоковий шифр на основі генератора BBS.  
2. Згенерувати два великих простих числа p, q, обчислити модуль n та випадкове число x.  
3. За  допомогою  створеної  програми  зашифрувати  та  розшифрувати  текстове 
повідомлення. 
"""

import secrets
from math import gcd


def generate_blum_prime(bit_length: int) -> int:
    """Генерація простого числа Блюма: p ≡ 3 (mod 4)."""
    while True:
        # Старший біт задає потрібну довжину, а біти 11 забезпечують остачу 3 mod 4.
        candidate = secrets.randbits(bit_length) | (1 << (bit_length - 1)) | 3
        # Перевіряємо, чи є випадкове число простим.
        if all(pow(base, candidate - 1, candidate) == 1
               for base in (2, 3, 5, 7, 11)):
            return candidate


class BBSGenerator:
    def __init__(self, modulus: int, seed: int):
        if gcd(seed, modulus) != 1:
            raise ValueError("Початкове число x повинне бути взаємно простим із модулем n")
        self.n = modulus
        # Початковий стан генератора: x_0 = seed^2 mod n.
        self.curr_state = pow(seed, 2, modulus)  # x_0 = x^2 mod n

    def get_next_bit(self) -> int:
        # Квадратимо стан і беремо його молодший біт.
        self.curr_state = pow(self.curr_state, 2, self.n)
        return self.curr_state & 1  # молодший біт, повертає 1, якщо число непарне, і 0, якщо парне

    def get_next_byte(self) -> int:
        byte_val = 0
        for _ in range(8):
            byte_val = (byte_val << 1) | self.get_next_bit()
        return byte_val

    def generate_gamma(self, num_bytes: int) -> bytes:
        return bytes(self.get_next_byte() for _ in range(num_bytes))


def apply_xor(data: bytes, gamma: bytes) -> bytes:
    # XOR тієї самої гамми використовується і для шифрування, і для розшифрування.
    return bytes(b1 ^ b2 for b1, b2 in zip(data, gamma))


def bbs_encrypt(plaintext: str, n: int, x: int) -> bytes:
    raw_bytes = plaintext.encode("utf-8")
    gamma = BBSGenerator(n, x).generate_gamma(len(raw_bytes))
    return apply_xor(raw_bytes, gamma)


def bbs_decrypt(ciphertext: bytes, n: int, x: int) -> str:
    gamma = BBSGenerator(n, x).generate_gamma(len(ciphertext))
    return apply_xor(ciphertext, gamma).decode("utf-8")


def main():
    bit_size = 256
    p = generate_blum_prime(bit_size)
    q = generate_blum_prime(bit_size)
    while p == q:
        q = generate_blum_prime(bit_size)
    
    n = p * q

    while True:
        x = secrets.randbelow(n - 2) + 2
        if gcd(x, n) == 1:
            break

    print("=== Завдання 1. BBS ===")
    print(f"p = {p}\n")
    print(f"q = {q}\n")
    print(f"n = {n}\n")
    print(f"Початкове x = {x}\n")

    user_msg = input("Enter text for encrypting: ")
    print(f"\nPlain text: {user_msg}")

    encrypted_data = bbs_encrypt(user_msg, n, x)
    print(f"Cyphertext (hex): {encrypted_data.hex()}")

    decrypted_text = bbs_decrypt(encrypted_data, n, x)
    print(f"Decrypted:     {decrypted_text}")
    print(f"Successful:          {decrypted_text == user_msg}")


if __name__ == "__main__":
    main()