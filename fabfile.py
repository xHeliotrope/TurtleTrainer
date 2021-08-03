from os import walk
from fabric import task
from trainer.genetic import genetic
from trainer.handler import FileHandler
from pprint import pprint

@task
def run(c):
    genetic.main()

@task
def scores(c):
    scores = []
    for root, _, files in walk('recordings'):
        try:
            reward = [f for f in files if '.0' in f]
            if float(reward[0]) and float(reward[0]):
                scores.append([root, reward[0]])
        except Exception as exc:
            pass
    scores.sort(key = lambda x: float(x[1]))
    pprint(scores)

@task
def clean(c):
    pass

@task
def record(c, generation, file_number):
    fh = FileHandler(generation=generation, file_number=file_number)
    fh.create_video()
