#!/usr/bin/env python3

from random import randint
from time import sleep

import retro
import numpy as np

from file_handler import FileHandler
from model import Model

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'


data_file = open('gamedata.txt', 'w+')

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


# associate actions with 'cooldown' times, 
# so that when an action is taken, 
# we know when it is possible to take the next action
# after that

ACTION_SPACE = {
    "b": 60,
    "null": 60,
    "select": 0,
    "start": 0,
    "up": 0,
    "down": 0,
    "left": 0,
    "right": 0,
    "a": 30
}


# get the action name of the button push array
# returns strings like 'jump' or 'right' or some shit
def get_action_name(pushed_index):
    keys = ACTION_SPACE.keys()
    return keys[pushed_index]

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

    forward = True
    done = 0
    cooldown_time = 0

    cooldown_timer = 0
    pushed_index = 0
    direction = 7

    iterator = 0
    attack_cooldown = 10
    jump_cooldown = 10
    
    # file to write data for neural net
    f = open('moves.txt', 'w+')

    while not done:
        attack_cooldown -= 1 
        jump_cooldown -= 1 
        iterator += 1

        # default action is do nothing
        sample_action = np.zeros(9, dtype=np.int8)
        sample_action[direction] = 1

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
        if iterator % 25 == 0 and jump_cooldown <= 0:
            sample_action[0] = 1
            # prevent special attacks
            sample_action[8] = 0
            attack_cooldown = 10

        # jump 2/3 of a time each second and turtle hasnt attacked recently
        if iterator % 21 == 0 and attack_cooldown <= 0:
            sample_action[8] = 1
            # prevent special attacks
            sample_action[0] = 0
            jump_cooldown = 10

        _obs, _rew, done, _info = env.step(sample_action)
        
        output_data = np.append(sample_action, _rew)

        data_file.write(str(output_data) + '\n')

    # create video file from replay
    #handler.create_video()


    # spin it
    #handler.play_video()

