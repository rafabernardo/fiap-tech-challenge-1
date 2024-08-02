import re


def validate_cpf(cpf):
    if cpf is None:
        return False

    cpf = "".join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    sum = 0
    for i in range(9):
        sum += int(cpf[i]) * (10 - i)
    digit_1 = (sum * 10) % 11
    if digit_1 == 10:
        digit_1 = 0

    sum = 0
    for i in range(10):
        sum += int(cpf[i]) * (11 - i)
    digit_2 = (sum * 10) % 11
    if digit_2 == 10:
        digit_2 = 0

    if int(cpf[9]) != digit_1 or int(cpf[10]) != digit_2:
        return False

    return True


def validate_email(email):
    if email is None:
        return False

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        return False

    return True
