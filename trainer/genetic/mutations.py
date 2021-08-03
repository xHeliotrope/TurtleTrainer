"""Custom mutation functions for altering probabilities

This function altered from:
https://github.com/DEAP/deap/blob/1.3.0/deap/tools/mutation.py#L95
"""
import random


def mutShiftIndices(individual, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            if i == 0:
                small_wiggle = random.randint(1, 7)
                if individual[0][1] > small_wiggle:
                    print(f'small wiggled: {small_wiggle}')
                    rearranged = (individual[0][1] - small_wiggle, individual[0][0] + small_wiggle)
            else:
                rearranged = (individual[i][2], individual[i][0], individual[i][1])
            individual[i] = rearranged

    return individual,
