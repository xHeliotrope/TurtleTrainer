#!/usr/bin/env python3
from time import sleep

import retro

from file_handler import FileHandler
from agent import BadAgent

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

    #game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
    #game_meta = '-1Player.Leo.Level1-000000'

    curious_histo = set()

    # create a file handlin object
    handler = FileHandler(game_name + game_meta)

    # rm TMNT video, if there is one
    handler.rm_video()
    # rm TMNT replay, if there is one
    handler.rm_backup()

    env = retro.make(game=game_name, record='.')
    env.reset()

    forward = True
    done = 0
    cumulative_reward = 0

    # 0.2126 R + 0.7152 G + 0.0722 B



    while not done:
        if forward:
            sample_action = env.action_space.sample()
            _obs, _rew, done, _info = env.step(sample_action)
            cumulative_reward += _rew

    # create video file from replay
    handler.create_video()

    sleep(10)

    # spin it
    handler.play_video()

