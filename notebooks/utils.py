from os import walk
from pprint import pprint

def get_scores():
    scores = []
    for root, _, files in walk('..recordings'):
        try:
            reward = [f for f in files if '.0' in f]
            if float(reward[0]) and float(reward[0]):
                scores.append([root, reward[0]])
        except Exception as exc:
            pass
    scores.sort(key = lambda x: float(x[1]))
    pprint(scores)
