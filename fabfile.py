from os import walk
from fabric import task
from trainer.genetic import genetic
from trainer.handler import FileHandler

@task
def run(c):
    genetic.main()

@task
def scores(c):
    for root, _, files in walk('recordings'):
        try:
            if float(files[0]) and float(files[0]):
                print(root, files[0])
        except Exception as exc:
            pass
@task
def record(c, generation, file_number):
    fh = FileHandler(generation=generation, file_number=file_number)
    fh.create_video()
