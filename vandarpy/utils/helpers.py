import re

PHONE_REGEX = re.compile(r'^(?:\+98|0)9\d{9}$')


def is_valid_phone_number(phone_number: str) -> bool:
    return bool(PHONE_REGEX.match(phone_number))


def is_valid_national_code(national_code: str) -> bool:
    if 8 <= len(national_code) < 10:
        national_code = '0' * (10 - len(national_code)) + national_code

    if len(national_code) != 10 or not national_code.isdigit():
        return False

    check = int(national_code[9])
    s = 0
    for i in range(9):
        s += int(national_code[i]) * (10 - i)
    s %= 11
    return (2 > s == check) or (s >= 2 and check + s == 11)


def is_valid_card_number(card_number: str) -> bool:
    if len(card_number) != 16 or not card_number.isdigit():
        return False

    s = 0
    for i in range(16):
        if i % 2 == 0:
            s += int(card_number[i]) * 2
            if int(card_number[i]) * 2 > 9:
                s -= 9
        else:
            s += int(card_number[i])
    return s % 10 == 0
