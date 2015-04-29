__author__ = 'cthulhu'
from Bot import Bot
import random


class RandomBot(Bot):

    def __init__(self):
        pass

    def get_move(self, board):

        min_value = 0
        max_value = len(board) - 1
        target = random.randint(min_value, max_value), random.randint(min_value, max_value)
        return target, False
