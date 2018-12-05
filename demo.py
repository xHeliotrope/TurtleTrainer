#!/usr/bin/env python3
from time import sleep

import retro
import numpy

from file_handler import FileHandler
from model import Model

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'


def make_game():
    env = retro.make(game=game_name, record='.')
    env.reset()
    return env

def make_video():
    handler = FileHandler(game_name + game_meta)
    handler.create_video()

def play_video():
    handler = FileHandler(game_name + game_meta)
    handler.play_video()


if __name__ == "__main__":

    game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
    game_meta = '-1Player.Leo.Level1-000000'

    # create a file handlin object
    handler = FileHandler(game_name + game_meta)

    # rm TMNT video, if there is one
    #handler.rm_video()
    # rm TMNT replay, if there is one
    #handler.rm_backup()

    env = retro.make(game=game_name, record='.')
    env.reset()

    f = open("moves.txt", "w+")
    forward = True
    done = 0
    cumulative_reward = 0
    i = 0
    while not done:
        i += 1
        sample_action = env.action_space.sample()
        f.write(numpy.array2string(sample_action) + '\n')
        _obs, _rew, done, _info = env.step(sample_action)
    print(i)

    # create video file from replay
    #handler.create_video()


    # spin it
    #handler.play_video()

