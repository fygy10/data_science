import random
import numpy as np
from time import time

#FIND THE MEAN OF A DATASET
#the largeer the dataset, the faster the function in from slowest to fastest

def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function executed in {(t2 - t1): .4f} seconds')
        return result
    return wrapper

@timer
def compute_mean(numbers):
    n = len(numbers)

    total = 0

    for value in numbers:
        total = total + value

    mean = total / n

    return mean

@timer
def compute_mean_faster(numbers):
    return sum(numbers) / len(numbers)


@timer
def compute_mean_fastest(numbers):
    return np.mean(numbers)


n = random.randint(1, 100000)
nums = [random.randint(1, 1000000) for _ in range(n)]
print(compute_mean(nums))
print(compute_mean_faster(nums))
print(compute_mean_fastest(nums))