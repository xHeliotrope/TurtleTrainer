import unittest

import retro

from trainer.handler import FileHandler
from trainer.handler import game_name
from trainer.model import Bot


class ModuleTest(unittest.TestCase):
    """The basic classes/functions of the module work as expected
    """
    def test_create_filehandler(self):
        fh = FileHandler()
        assert type(fh) == FileHandler

    def test_create_env(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        assert type(env) == retro.retro.RetroEnv

    def test_create_bot(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        reward = 0
        bot = Bot(env, reward, fh)
        assert type(bot) == Bot
