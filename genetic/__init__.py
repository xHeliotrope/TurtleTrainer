"""Base code for genetic programming
"""
import random

def random_tuple(l, sigma):
    """returns a tuple of random numbers.
     - the tuple is of length `l`
     - the sum of the numbers in the tuple is `sigma`

    Arguments:
        l (int): length of the tuple
        sigma (int): sum of all the values in the tuple
    """
    percentage_indices = [0, sigma]
    random_list = []
    # populate numrs with l integers, that are randomly distributed between 0 and sigma
    for _ in range(l - 1):
        percentage_indices.append(random.randint(0, sigma))
    percentage_indices.sort()
    random_list = [percentage_indices[index + 1] - percentage_indices[index] for index in range(l)]
    return tuple(random_list)

