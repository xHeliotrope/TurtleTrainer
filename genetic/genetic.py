#!/usr/bin/env python3
import random
from pprint import pprint

import retro

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from turtles import StaticProbabilityTurtle
from file_handler import FileHandler

# constants for crossing and mating individuals
CXPB = 0.5
MUTPB = 0.2

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'

creator.create("ScoreMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.ScoreMax)

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

# the 8 attributes a StaticProbabilityTurtle Individual needs to be configured
# each is a state transition variable, with values 0 -> 100 being a percentage
toolbox = base.Toolbox()

toolbox.register("attr_jump_and_attack", random_tuple, 2, 100)
toolbox.register("attr_None_vert", random_tuple, 3, 100)
toolbox.register("attr_None_horiz", random_tuple, 3, 100)
toolbox.register("attr_left", random_tuple, 3, 100)
toolbox.register("attr_right", random_tuple, 3, 100)
toolbox.register("attr_up", random_tuple, 3, 100)
toolbox.register("attr_down", random_tuple, 3, 100)


toolbox.register(
        "individual",
        tools.initCycle,
        creator.Individual,
        (
            toolbox.attr_jump_and_attack,
            toolbox.attr_None_vert,
            toolbox.attr_None_horiz,
            toolbox.attr_left,
            toolbox.attr_right,
            toolbox.attr_up,
            toolbox.attr_down
        ),
        n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# for the saving of videos and backups
def evaluate_turtle(individual):
    """evaluates the success of a given turtlebot

    Arguments:
      - individual (<subclass of Turtle obj>) : a postgame turtle, to be evaluated

    Returns:
      - (tuple): tuple with equal length of the weights (note the comma)
    """
    file_handl = FileHandler(file_number=random.randint(0, 1000000))
    file_handl.create_video_dir()
    turtle = StaticProbabilityTurtle(file_handl, attribute_list=individual)
    record_file = './{path}{number}'.format(
        path=file_handl.video_path,
        number=str(file_handl.file_number)
    )

    env = retro.make(game=game_name, record=record_file)
    env.reset()

    turtle.run_simulation(env)
    print(file_handl.file_number)
    print(turtle.reward)
    print(turtle.__dict__)
    print('==============')
    return turtle.reward,

toolbox.register("evaluate", evaluate_turtle)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    pop = toolbox.population(n=100)
    # evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    fits = [ind.fitness.values[0] for ind in pop]
    return pop, fitnesses

stuff = main()
pprint(stuff)