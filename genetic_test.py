#!/usr/bin/env python3

import random

from deap import tools
from deap import creator
from deap import base

creator.create("StuffMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.StuffMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

