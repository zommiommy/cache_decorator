import random
import string

def random_string(length):
    # choose from all lowercase letter
    letters = string.hexdigits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str