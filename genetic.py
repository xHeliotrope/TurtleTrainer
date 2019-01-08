import random
from deap import algorithms, base, creator, tools
from agent import BasicProbabilityBot

creator.create("RewardMax", base.Fitness, weights(1.0,))
creator.create("Individual", BasicProbabilityBot, fitness=creator.RewardMax)

