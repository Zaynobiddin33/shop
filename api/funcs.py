from random import sample
from string import ascii_letters, digits

def code_generate(num = 50):
    result = sample(ascii_letters+digits, num)
    return "".join(result)