#!/usr/bin/env python3

from random import randint
from time import sleep

import retro
import numpy as np

from file_handler import FileHandler
from agents import BasicProbabilityBot

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


"""
for reference, the actions are:
  0 - "b"
  1 - "null"
  2 - "select"
  3 - "start"
  4 - "up"
  5 - "down"
  6 - "left"
  7 - "right"
  8 - "a"
"""

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

    done = 0
    direction = 7

    action_number = 0
    attack_cooldown = 10
    jump_cooldown = 10

    while not done:

        # default action is do nothing
        sample_action = np.zeros(9, dtype=np.int8)
        # move left or right
        sample_action[direction] = 1

        attack_cooldown -= 1 
        jump_cooldown -= 1 
        action_number += 1

        # switch from right to left
        # 1/10 times
        if direction == 7:
            switch_direction = randint(0, 10)
            if switch_direction == 1:
                direction = 6 

        # switch from left to right
        # switch 1/5 times
        if direction == 6:
            switch_direction = randint(0, 5)
            if switch_direction == 1:
                direction = 7 

        # wiggle up and down 1/3 of the time
        wiggle = randint(0,3)
        if wiggle == 1:
            sample_action[5] = 1
        elif wiggle == 2:
            sample_action[4] = 1

        # attack 1/46 times
        # (roughly 2/3 of a second)
        if action_number % 25 == 0 and jump_cooldown <= 0:
            sample_action[0] = 1
            # prevent special attacks
            sample_action[8] = 0
            attack_cooldown = 10

        # jump 2/3 of a time each second and turtle hasnt attacked recently
        if action_number % 21 == 0 and attack_cooldown <= 0:
            sample_action[8] = 1
            # prevent special attacks
            sample_action[0] = 0
            jump_cooldown = 10

        _obs, _rew, done, _info = env.step(sample_action)

        if _info['score'] != 0:
            done = True
        
        output_data = np.append(sample_action, _rew)

        data_file.write(str(output_data) + '\n')

    # create video file from replay
    #handler.create_video()

    # spin it
    #handler.play_video()

