import os
from django.utils.crypto import get_random_string


def get_secret_key(path_to_sk):
    if not os.path.exists(path_to_sk):
        with open(path_to_sk, 'a') as sk_file:
            chars = 'abcdefghijklmnopqrstuvwxyz0123789!@#$%^&*(-_=+)'
            secret_key = get_random_string(50, chars)
            sk_file.write(secret_key)
    else:
        with open(path_to_sk, 'r') as sk_file:
            secret_key = sk_file.read()

    return secret_key
