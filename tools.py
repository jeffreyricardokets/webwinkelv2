import random
import string

def make_random_text_generator(i):
    letter = string.ascii_letters
    return ''.join(random.choice(letter) for k in range(i))

def make_random_number_generator(i):
    number = string.digits
    return ''.join(random.choice(number) for k in range(i))