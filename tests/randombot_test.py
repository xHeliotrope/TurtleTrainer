import unittest

import retro

from trainer.handler import FileHandler
from trainer.genetic.genetic import game_name
from trainer.model.random_bot import RandomBot


class RandomBotTest(unittest.TestCase):
    """The RandomBot functions
    """
    def test_create_randombot(self):
        """
        RandomBot(
                env,
                file_handler,
                transitions,
                cooldowns={'jump': 10, 'attack': 10},
                directions={'4': 0, '5': 0, '6': 0, '7': 0},
                **kwargs,
        )

            toolbox.register("attr_jump_and_attack", random_tuple, 2, 100)
            toolbox.register("attr_None_vert", random_tuple, 3, 100)
            toolbox.register("attr_None_horiz", random_tuple, 3, 100)
            toolbox.register("attr_left", random_tuple, 3, 100)
            toolbox.register("attr_right", random_tuple, 3, 100)
            toolbox.register("attr_up", random_tuple, 3, 100)
            toolbox.register("attr_down", random_tuple, 3, 100)
        """
        fh = FileHandler()
        states = (1, 33, 66)
        transitions = [(1,99), states, states, states, states, states, states]
        env = retro.make(game=game_name, record='./' + fh.root_path)
        bot = RandomBot(env, fh, transitions)
        assert type(bot) == RandomBot

    # def test_create_env(self):
    #     fh = FileHandler()
    #     env = retro.make(game=game_name, record='./' + fh.root_path)
    #     assert type(env) == retro.retro.RetroEnv

    # def test_create_bot(self):
    #     fh = FileHandler()
    #     env = retro.make(game=game_name, record='./' + fh.root_path)
    #     reward = 0
    #     bot = Bot(env, reward, fh)
    #     assert type(bot) == Bot
