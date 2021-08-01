import random

import retro

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from . import random_tuple

from model.random_turtle import RandomTurtle
from file_handler import FileHandler


game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'

creator.create("ScoreMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.ScoreMax)

# the 8 attributes a RandomTurtle Individual needs to be configured
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
    # setup the file handler for writing data locally
    file_handler = FileHandler(generation=individual.generation, file_number=random.randint(0, 10000000))
    file_handler.create_video_dir()
    file_handler.write_turtle_stats(individual)

    # setup the gym retro environment
    env = retro.make(game=game_name, record='./' + file_handler.root_path)
    env.reset()

    turtle = RandomTurtle(env, file_handler, attribute_list=individual)
    turtle.run_simulation()

    print('==============')
    print('REWARD: ', str(turtle.reward))
    print('==============')
    file_handl.write_turtle_score(turtle.reward)
    return turtle.reward,

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("evaluate", evaluate_turtle)

def main():
    population = toolbox.population(n=20)
    # number of generations
    NGEN = 20
    # crossing probability
    CXPB = 0.5
    # mating probability
    MUTPB = 0.2
    for gen in range(NGEN):
        # select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # add the generation attribute so that can be passed to the
        # file_handler
        [setattr(ind, 'generation', gen) for ind in offspring]
        offspring = list(map(toolbox.clone, offspring))

        # CROSSING
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        # MATING
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        fits = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fits):
            ind.fitness.values = fit

        print('offspring: ')
        print(len(offspring))
        print([ind for ind in offspring])
        print('population: ')
        print(len(population))
        print([ind for ind in population])
        population[:] = offspring
