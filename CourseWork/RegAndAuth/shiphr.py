def encrypt(text, key):
    cyrillic_abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ,.!?1234567890@#$%^&*()_+:;/[]{}~`<>|"
    encrypted = ""
    for i in text:
        if i not in cyrillic_abc:
            return encrypted
    if len(text) == 0 or len(key) == 0 or len(key) > len(text):
        return encrypted
    for i in key:
        if i not in cyrillic_abc:
            return encrypted
    else:
        letter_to_index = dict(zip(cyrillic_abc, range(len(cyrillic_abc))))
        index_to_letter = dict(zip(range(len(cyrillic_abc)), cyrillic_abc))
        split_text = [
            text[i: i + len(key)] for i in range(0, len(text), len(key))
        ]

        for each_split in split_text:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(cyrillic_abc)
                encrypted += index_to_letter[number]
                i += 1

        return encrypted


def decrypt(shiphr, key):
    cyrillic_abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ,.!?1234567890@#$%^&*()_+:;/[]{}~`<>|"
    decrypted = ""
    for i in shiphr:
        if i not in cyrillic_abc:
            return decrypted
    for i in key:
        if i not in cyrillic_abc:
            return decrypted
    if len(shiphr) == 0 or len(key) == 0:
        return decrypted
    else:
        letter_to_index = dict(zip(cyrillic_abc, range(len(cyrillic_abc))))
        index_to_letter = dict(zip(range(len(cyrillic_abc)), cyrillic_abc))
        split_encrypted = [
            shiphr[i: i + len(key)] for i in range(0, len(shiphr), len(key))
        ]

        for each_split in split_encrypted:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(cyrillic_abc)
                decrypted += index_to_letter[number]
                i += 1

        return decrypted
