from os import walk
import re

def list_all_scores():
    scores = {num: [] for num in range(20)}
    for (root, dirs, files) in walk('../recordings'):
        if('stats.txt' in files and len(files) == 3):
            gen = re.search('recordings/(.*)/', root).group(1)
            try:
                filescore = int(float(files[0]))
            except ValueError:
                try:
                    filescore = int(float(files[1]))
                except ValueError:
                    try:
                        filescore = int(float(files[2]))
                    except ValueError:
                        print("well schucks")
            scores[int(gen)].append(filescore)

    return scores

