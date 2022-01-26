def text_and_key(text, key):
    if text == '' or key == '':
        key_m = 'Error'
        return key_m
    else:
        key_m = ""
        j = 0
        for i in range(len(text)):
            if 1040 <= ord(text[i]) <= 1071:
                if j < len(key):
                    key_m += key[j].upper()
                    j += 1
                else:
                    j = 0
                    key_m += key[j].upper()
                    j += 1
            elif 1072 <= ord(text[i]) <= 1103:
                if j < len(key):
                    key_m += key[j]
                    j += 1
                else:
                    j = 0
                    key_m += key[j]
                    j += 1
            else:
                key_m += " "
        return key_m


def create_table():
    table = []
    for i in range(32):
        table.append([])
    for row in range(32):
        for column in range(32):
            if (row + 1040) + column > 1071:
                table[row].append(chr((row + 1040) + column - 32))
            else:
                table[row].append(chr((row + 1040) + column))
    return table


def create_table_1():
    table = []
    for i in range(32):
        table.append([])
    for row in range(32):
        for column in range(32):
            if (row + 1072) + column > 1103:
                table[row].append(chr((row + 1072) + column - 32))
            else:
                table[row].append(chr((row + 1072) + column))
    return table


def shiphr_encryption(message, mapped_key):
    table = create_table()
    table1 = create_table_1()
    enc_text = ""
    if mapped_key == 'Error':
        return enc_text
    for i in range(len(message)):
        # текст и ключ- заглавные
        if 1071 >= ord(message[i]) >= 1040:
            row = ord(message[i]) - 1040
            column = ord(mapped_key[i]) - 1040
            enc_text += table[row][column]
        # текст и ключ- строчные
        elif 1072 <= ord(message[i]) <= 1103:
            row = ord(message[i]) - 1072
            column = ord(mapped_key[i]) - 1072
            enc_text += table1[row][column]
        else:
            enc_text += message[i]
    return enc_text
