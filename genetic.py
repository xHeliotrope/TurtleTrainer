#!/usr/bin/env python3

import random

import retro

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from turtles import StaticProbabilityTurtle
from file_handler import FileHandler

file_handler = FileHandler()

# constants for crossing and mating individuals
CXPB = 0.5
MUTPB = 0.2

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'

creator.create("ScoreMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.ScoreMax)

# a place to register all of the genetic functions and classes
toolbox = base.Toolbox()

# the 8 attributes a StaticProbabilityTurtle Individual needs to be configured
# each is a state transition variable, with values 0 -> 100 being a percentage

def random_tuple(length, maximum):
    """random int combinations that add to a number

    Arguments:
        number (int): 
    """
    number_one = random.randint(0, number)
    number_two = random.randint(
    

toolbox.register("attr_ud_from_up", random.randint, 0, 50)
toolbox.register("attr_ud_from_down", random.randint, 0, 50)
toolbox.register("attr_ud_from_None", random.randint, 0, 50)
toolbox.register("attr_lr_from_left", random.randint, 0, 50)
toolbox.register("attr_lr_from_right", random.randint, 0, 50)
toolbox.register("attr_lr_from_None", random.randint, 0, 50)
toolbox.register("attr_jump", random.randint, 0, 100)
toolbox.register("attr_attack", random.randint, 0, 100)

toolbox.register(
        "individual",
        tools.initCycle,
        creator.Individual,
        (
            toolbox.attr_up_to_down,
            toolbox.attr_up_to_None,
            toolbox.attr_down_to_up,
            toolbox.attr_down_to_None,
            toolbox.attr_None_to_up,
            toolbox.attr_None_to_down,
            toolbox.attr_to_jump,
            toolbox.attr_to_attack
        ),
        n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate_turtle(individual):
    """evaluates the success of a given turtlebot

    Arguments:
      - individual (<subclass of Turtle obj>) : a postgame turtle, to be evaluated

    Returns:
      - (tuple): tuple with equal length of the weights
    """
    cooldowns = {
        'attack': 10,
        'jump': 10
    }
    from pprint import pprint
    pprint(individual)
    turtle = StaticProbabilityTurtle(cooldowns, file_handler)
    env = retro.make(game=game_name)
    env.reset()
    print(turtle.horizontal_transitions)
    turtle.run_simulation(env)
    return turtle.reward,

toolbox.register("evaluate", evaluate_turtle)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    pop = toolbox.population(n=10)
    # evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    fits = [ind.fitness.values[0] for ind in pop]
    return pop, fitnesses

main()
