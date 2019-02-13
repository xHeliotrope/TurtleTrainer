#!/usr/bin/env python3

from os import walk

from genetic import genetic

#genetic.main()

def list_all_scores():
    scores = []
    skip_root = True
    for root, dirs, files in walk('recordings/0'):
        if skip_root:
          skip_root = False
        else:
            if(len(files) == 3):
                scores.append(int(float(files[0])))
    scores.sort()
    print(scores)
