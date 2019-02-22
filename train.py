import random
from collections import namedtuple

import torch
import retro

from file_handler import FileHandler
from model import neural_turtle
from model import utils

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'

def main():
    dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    file_handl = FileHandler(file_number=random.randint(0, 10000000))
    file_handl.create_video_dir()

    env = retro.make(game=game_name+game_meta, record='./' + file_handl.root_path)
    env.reset()

    q_func = neural_turtle.DeepQTurtle
    q = q_func().type(dtype)


    optimizer_spec = namedtuple("OptimizerSpec", ["constructor", "kwargs"])
    optimizer = optimizer_spec(q_func.parameters(), **optimizer_spec)

    replay_buff = utils.ReplayBuffer(size=1000000, frame_history_len=4)

