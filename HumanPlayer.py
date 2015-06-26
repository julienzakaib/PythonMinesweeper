__author__ = 'cthulhu'
from Bot import Bot
import random


class HumanPlayer(Bot):

    def __init__(self):
        pass

    def get_move(self, board):

		# Prompt
        user = input("Your Move [ <row_number> <column_number> ] : ").split()

        target = int(user[0]), int(user[1])
        if len(user) == 3:
            flag_value = user[2]
        else:
            flag_value = "false"

        flag = True if flag_value.lower() == "true" else False
		
        return target, flag
