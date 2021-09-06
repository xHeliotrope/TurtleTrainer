"""Base code for genetic programming

for numpy usage here, see: 
https://numpy.org/doc/stable/reference/random/index.html#random-quick-start
"""
from numpy.random import default_rng
rng = default_rng()


def random_tuple(tuple_length, sigma=100):
    """returns a tuple of random numbers.
     - the tuple is of length `tuple_length`
     - the sum of the numbers in the tuple is `sigma`

    Arguments:
        tuple_length (int): length of the tuple
        sigma (int): sum of all the values in the tuple
    """
    percentage_indices = [0, sigma]
    random_list = []
    # populate numbers with l integers that are randomly distributed between 0 and sigma
    for _ in range(tuple_length - 1):
        percentage_indices.append(rng.integers(low=0, high=sigma + 1))  # numpy randint is high-end exclusive
    percentage_indices.sort()
    random_list = [percentage_indices[index + 1] - percentage_indices[index] for index in range(tuple_length)]
    rng.shuffle(random_list)
    return tuple(random_list)


def complete_uniform_probability(tuple_length, sigma=100):
    """this function may be too compute and space expensive to run on-the-fly
    """
    pass


def end_weighted_probability(tuple_length, sigma=100):
    """what im calling 'double-end-weighted' is that one probability
    is uniformly distributed between 0 and 100 (call this k), and then the
    next probability is weighted between 0 and (100 - k), and the last one is
    whats left
    """
    probabilities = []
    for _ in range(tuple_length - 1):
        probabilities.append(rng.integers(low=0, high=(sigma - sum(probabilities) + 1)))
    probabilities.append(sigma - sum(probabilities))
    rng.shuffle(probabilities)
    return tuple(probabilities)

