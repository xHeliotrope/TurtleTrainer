import random
from deap import algorithms, base, creator, tools
from agent import GamerTurtle

creator.create("RewardMax", base.Fitness, weights(1.0,))
creator.create("Individual", GamerTurtle, fitness=creator.RewardMax)


