import numpy as np
from time import time
import random

#EXPONENT CALCULATION

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function executed in {(t2 - t1): .4f} seconds')
        return result
    return wrapper


@timer
def exponent(base, exp):
    result = 1

    for _ in range(exp):
        result = result * base

    return result
    

@timer
def exponent_faster(base, exp):
    return base ** exp


@timer
def exponent_fastest(base, exp):
    return np.power(base, exp)


base = random.randint(1, 1000) 
exp = random.randint(1, 1000)

print(exponent(base, exp))
print(exponent_faster(base, exp))
print(exponent_fastest(base, exp))