#!/usr/bin/env python3

from random import randint
from time import sleep

import retro
import numpy as np

from file_handler import FileHandler
from turtles import StaticProbabilityTurtle

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

    handler = FileHandler(game_name + game_meta)

    env = retro.make(game=game_name, record='.')
    env.reset()

    # action cooldowns
    cooldowns = {
        'attack': 10,
        'jump': 10
    }
    
    bot = StaticProbabilityTurtle(cooldowns, handler)
    bot.run_simulation(env)
