from random import randint


def get_verification_code(customer):
    random_number = randint(1000,9999)
    return random_number