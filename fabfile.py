from os import walk
from fabric import task
from trainer.genetic import genetic

@task
def run(c):
    genetic.main()

@task
def list_all_scores(c):
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
