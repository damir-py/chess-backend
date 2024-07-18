import random


def generate_otp_code():
    first_digit = str(random.randint(1, 9))
    other_digits = [str(random.randint(0, 9)) for _ in range(4)]
    return first_digit + ''.join(other_digits)


