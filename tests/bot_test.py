import retro

from trainer.handler import FileHandler
from trainer.genetic.genetic import game_name
from trainer.model import Bot

def test_create_filehandler():
    fh = FileHandler()
    assert type(fh) == FileHandler

def test_create_env():
    fh = FileHandler()
    env = retro.make(game=game_name, record='./' + fh.root_path)
    assert type(env) == retro.retro.RetroEnv

def test_create_bot():
    fh = FileHandler()
    env = retro.make(game=game_name, record='./' + fh.root_path)
    reward = 0
    bot = Bot(env, reward, fh)
    assert type(bot) == Bot
