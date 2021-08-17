import random

import retro

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from . import random_tuple

from trainer.handler import FileHandler
from trainer.model.probability.random_bot import RandomBot
from trainer.genetic import mutations


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
    env = retro.make(game=file_handler.game_name, record='./' + file_handler.root_path)
    env.reset()

    turtle = RandomBot(env, file_handler, {}, attribute_list=individual)
    turtle.run_simulation()

    print('==============')
    print('REWARD: ', str(turtle.reward))
    print('==============')
    file_handler.write_turtle_score(turtle.reward)
    return turtle.reward,

toolbox.register("mate", tools.cxTwoPoint)
# indices will be shuffled at least once with probility (1-.10)^7
toolbox.register("mutate", mutations.mutShiftIndices, indpb=0.10)
toolbox.register("select", tools.selBest)
toolbox.register("evaluate", evaluate_turtle)

def main():
    population = toolbox.population(n=20)
    # number of generations
    NGEN = 20
    # crossing probability
    CXPB = 0.5
    # mating probability
    MUTPB = 0.2
    first_run = True
    for gen in range(NGEN):
        # select the next generation individuals
        if first_run:
            offspring = toolbox.select(population, 20)
        if not first_run:
            offspring = toolbox.select(population, 15)
        # make clones the offspring (for object-oriented reasons)
        offspring = list(map(toolbox.clone, offspring))

        # cull the weak
        strong_offspring = []
        for child in offspring:

            # include the child if the child had a non-zero score
            # (first-gen wont have a score so include them by default)
            if first_run or float(child.fitness.values[0]):
                strong_offspring.append(child)

        first_run = False
        # replace the weak
        offspring = strong_offspring
        new_children = NGEN - len(strong_offspring)
        if new_children:
            print(f'replacing {new_children} failed children this round')
            new_children = toolbox.population(n=new_children)
        else:
            new_children = []

        # CROSSING
        #for child1, child2 in zip(offspring[::2], offspring[1::2]):
        #    if random.random() < CXPB:
        #        toolbox.mate(child1, child2)
        #        print(f'making {child1} and {child2} invalid via crossing')
        #        del child1.fitness.values
        #        del child2.fitness.values
        
        # MATING
        for mutant in offspring:
            if random.random() < MUTPB:
                print(f'making {mutant} invalid via mutation')
                toolbox.mutate(mutant)
                del mutant.fitness.values


        # adding in new children
        offspring.extend(new_children)
        # add the generation attribute for the FileHandler
        [setattr(ind, 'generation', gen) for ind in offspring]

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        print(f'{len(invalid_ind)} invalid individuals')
        fits = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fits):
            ind.fitness.values = fit

        population[:] = offspring
