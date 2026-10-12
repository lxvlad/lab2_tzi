# Завдання 2. Варіант 8: скремблер x^5 + x^4 + x + 1 (n = 5)
import random

N = 5


def lfsr_step(state):
    """Один такт роботи регістра для x^5 + x^4 + x + 1."""
    out_bit = state[0]  # вихідний біт (перша комірка)
    
    # Зворотний зв'язок: індекси 0, 1 та 4 (відповідають x^0, x^1 та x^4)
    feedback = state[0] ^ state[1] ^ state[4]
    
    # Зсуваємо список вліво і додаємо новий біт у кінець
    new_state = state[1:] + [feedback]
    return new_state, out_bit, feedback


def generate_keystream(init_state, length, show_table=False):
    """Генерує потік бітів ключа (гаму) потрібної довжини і (за потреби) друкує таблицю."""
    state = list(init_state)
    gamma = []

    if show_table:
        print(f"{'Такт':>4} | {'Стан регістра':^13} | {'ЗЗ':>2} | {'Вихід':>5}")
        print("-" * 34)

    for step in range(length):
        current_str = " ".join(map(str, state))
        state, out_bit, fb = lfsr_step(state)
        gamma.append(out_bit)

        if show_table:
            print(f"{step:>4} |   {current_str}   | {fb:>2} | {out_bit:>5}")

    return gamma


def text_to_bits(text):
    """Переводить текст у список із 0 та 1."""
    bits = []
    for byte in text.encode("utf-8"):
        # format(byte, '08b') перетворює число (напр. 72) у рядок з 8 бітів ('01001000')
        for b in format(byte, "08b"):
            bits.append(int(b))
    return bits


def bits_to_text(bits):
    """Переводить список із 0 та 1 назад у текст."""
    byte_list = []
    for i in range(0, len(bits), 8):
        byte_str = "".join(map(str, bits[i:i + 8]))
        byte_list.append(int(byte_str, 2))
    return bytes(byte_list).decode("utf-8")


def xor_bits(bits_a, bits_b):
    """Побітовий XOR двох списків."""
    return [a ^ b for a, b in zip(bits_a, bits_b)]


def main():
    print("Варіант 8: скремблер x^5 + x^4 + x + 1 (n = 5)\n")

    # 1. Задаємо початковий стан (ключ) з 5 бітів
    raw = input("Введіть ключ з 5 бітів (напр. 10110, Enter = випадковий): ").strip()
    if raw:
        key = [int(c) for c in raw]
    else:
        key = [random.randint(0, 1) for _ in range(N)]
        if not any(key):  # щоб випадково не випали всі нулі [0, 0, 0, 0, 0]
            key[0] = 1

    print("Початковий ключ:", "".join(map(str, key)), "\n")

    # 2. Виводимо таблицю роботи регістра (наприклад, на 15 тактів)
    print("Таблиця роботи регістра:")
    generate_keystream(key, 15, show_table=True)

    # 3. Шифрування та розшифрування
    message = input("\nВведіть повідомлення: ")
    plain_bits = text_to_bits(message)

    # Генеруємо стільки бітів ключа, скільки бітів у нашому повідомленні
    gamma = generate_keystream(key, len(plain_bits))

    # Шифруємо (текст XOR гама)
    cipher_bits = xor_bits(plain_bits, gamma)

    # Розшифровуємо (шифротекст XOR та сама гама)
    decrypted_bits = xor_bits(cipher_bits, gamma)
    decrypted_text = bits_to_text(decrypted_bits)

    print(f"\nВідкритий текст:  {message}")
    print(f"Біти тексту:      {''.join(map(str, plain_bits))}")
    print(f"Згенерована гама: {''.join(map(str, gamma))}")
    print(f"Шифротекст (біти):{''.join(map(str, cipher_bits))}")
    print(f"Розшифровано:     {decrypted_text}")


if __name__ == "__main__":
    main()