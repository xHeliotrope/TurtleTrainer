#!/usr/bin/env python3

import random
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from turtles import StaticProbabilityTurtle

creator.create("RewardMax", base.Fitness, weights=(1.0,))
creator.create("Individual", StaticProbabilityTurtle, fitness=creator.RewardMax)
toolbox = base.Toolbox()

# the 8 attributes a StaticProbabilityTurtle Individual needs to be configured
# each is a state transition variable, with values 0 -> 100 being a percentage
toolbox.register("attr_up_to_down", random.randint, 0, 100)
toolbox.register("attr_up_to_None", random.randint, 0, 100)
toolbox.register("attr_down_to_up", random.randint, 0, 100)
toolbox.register("attr_down_to_None", random.randint, 0, 100)
toolbox.register("attr_None_to_up", random.randint, 0, 100)
toolbox.register("attr_None_to_down", random.randint, 0, 100)
toolbox.register("attr_to_jump", random.randint, 0, 100)
toolbox.register("attr_to_attack", random.randint, 0, 100)


def eval_turtlebot(individual):
    """evaluates the success of a given turtlebot

    Arguments:
      - individual (<subclass of Turtle obj>) : a postgame turtle, to be evaluated

    Returns:
      - (tuple): tuple with equal length of the weights
    """
    return turtle.reward,

