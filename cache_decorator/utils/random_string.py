import secrets
import string

def random_string(length):
    return secrets.token_hex(length)