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
    # start with 2 numbers to 'bookend' the list
    numrs = [0, sigma]
    random_list = []
    # populate numrs with l integers, that are randomly distributed between 0 and sigma
    [ numrs.append(random.randint(0, sigma)) for _ in range(l - 1) ]
    numrs.sort()
    # populate random_list
    random_list = [numrs[index+1] - numrs[index] for index in range(l)]
    return tuple(random_list)

