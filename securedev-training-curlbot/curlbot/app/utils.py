import random
import string

def get_random_string(length=20):
    charset = string.ascii_letters+string.digits
    return ''.join(random.choice(charset) for i in range(length))