from os import walk
import re

def list_all_scores():
    scores = {num: [] for num in range(20)}
    for (root, dirs, files) in walk('../recordings'):
        if('stats.txt' in files and len(files) == 3):
            gen = re.search('recordings/(.*)/', root).group(1)
            scores[int(gen)].append(int(float(files[0])))

    return scores

