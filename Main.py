__author__ = 'cthulhu'
import Exceptions

from Board  import Board
from Cell   import Cell
from RandomBot import RandomBot

# Game Config
size = 5
nMines = 2

# Instanciate your Bot here
player = RandomBot()

# Instanciate Minesweeper Board
minesweeper = Board(size, nMines)

first_turn = True

print("Starting Game")
minesweeper.reveal()
print("========================")
minesweeper.show()
print("========================")

# Start Game
while True:

    try:
        # Get Move from player
        # target_cell   : Cell or tuple(row, column)
        # is_flag       : Boolean
        target_cell, is_flag = player.get_move(minesweeper)

        # Print chosen action
        if isinstance(target_cell, Cell):
            i, j = minesweeper.get_cell_coord(target_cell)
        else:
            i, j = target_cell

        print("Action Chosen : ({}, {}) , Flag : {}".format(i, j, is_flag))
        if first_turn:
            print("First Move")

        # Apply Action
        # Result is Boolean : True = blew up a mine , False = you're fine
        # todo : improve this - maybe raise exception?
        try:
            minesweeper.player_action(target_cell, is_flag, first_turn)

        except Exceptions.YouBlewUp as BOOM:
            print(BOOM)
            minesweeper.reveal()
            break

        if minesweeper.is_solved():
            print("You Win !")
            minesweeper.reveal()
            break
        else:
            minesweeper.show()
            print("========================================\n")

    # Catch exceptions to help player's bot spot errors easily
    except (Exceptions.IndicesOutOfBoundsException, Exceptions.InvalidFlagTarget) as e:
        print(e)
        break

    # Flip the 'first_turn' flag when player actually reveals a cell
    first_turn = first_turn and is_flag

