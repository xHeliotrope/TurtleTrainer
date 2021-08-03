"""Custom mutation functions for altering probabilities

This function altered from:
https://github.com/DEAP/deap/blob/1.3.0/deap/tools/mutation.py#L95
"""
import random


def mutShuffleIndexesSkipZero(individual, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            swap_indx = random.randint(0, size - 2)
            # skip swapping with the 0-indexed tuple
            if i == 0 or swap_indx == 0:
                continue
            if swap_indx >= i:
                swap_indx += 1
            individual[i], individual[swap_indx] = \
                individual[swap_indx], individual[i]

    return individual,
