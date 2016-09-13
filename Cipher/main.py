
def to_numbers(char_list):
    ascii_list = []
    for x in char_list:
        ascii_list.append(ord(x))
    return ascii_list


def to_letters(num_list):
    letter_list = []
    for x in num_list:
        letter_list.append(chr(x))
    return letter_list


def caesar_cipher(key, ascii_list, dictionary):

    ASCII_FLOOR = 65
    cipher_text = []

    for x in ascii_list:
        x -= key
        if x < ASCII_FLOOR:
            x += 26
        cipher_text.append(x)

    dict_key = "Key {0}".format(key)
    dictionary[dict_key] = cipher_text

    return dictionary, dict_key

s = 'DRPWPWXHDRDKDUBKIHQVQRIKPGWOVOESWPKPVOBBDVVVDXSURWRLUEBKOLVHIHBKHLHBLNDQRFLOQ'
s = to_numbers(list(s))
ciphered_text = {}
for i in range(26):
    temp = caesar_cipher(i, s, ciphered_text)
    ciphered_text[temp[1]] = temp[0], to_letters((temp[0])[temp[1]])

ciphered_text
