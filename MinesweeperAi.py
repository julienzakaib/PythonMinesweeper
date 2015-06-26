__author__ = 'cthulhu'
from Bot import Bot
import random


class MinesweeperAi(Bot):

    def __init__(self):
        self.first_move = True

    # This method will be called once per game loop
    # The return value should be a tuple of the form (target_cell, flag)
    # @return target_cell   : either a Cell object or a coordinate tuple of the form (row_index, column_index)
    # @return flag          : boolean - True meaning "toggle flag" and false meaning "reveal this cell"
    #
    # example return values : return ((0,0), False) -> reveal cell board[0][0]
    #                       : cell = board[0][0] ... return (cell, False) -> reveal cell board[0][0]
    #                       : return ((1,2), True) -> toggle flag on cell board[1][2]
    #
    # @param <Board> board : 2 dimensional tuple of Cell objects
    # IMPORTANT : no cheating ! There are methods on the Cell class which would allow you to know the
    # internal state of the cell (such as the fact that it is a mine, empty or a number), they are "reserved" for the Board
    def get_move(self, board):

        # Set index bounds
        min_value = 0
        max_value = len(board) - 1

        # First turn case
        if self.first_move:
            target = random.randint(min_value, max_value), random.randint(min_value, max_value)
            return target, False

        #############################################################
        #															#
        # Examples for how to work with the Board and Cell classes  #
        #															#
        #############################################################

        # Get all hidden cells
        hidden = [cell for row in board for cell in row if cell.is_hidden()]

        # Get all visible cells
        visible = [cell for row in board for cell in row if cell.is_visible()]

        # Get all revealed Number cells with a for loop
        numbers = []
        for row in board:
            for cell in row:
                if cell.is_visible() and cell.is_number():
                    numbers.append(cell)

        # Note : always check for cell.is_hidden() or cell.is_visible() before using the following methods
        # cell.is_number()
        # cell.is_empty()
        # cell.is_mine() -> technically I don't think you should ever use this
        #
        # Because these methods will tell you if a Cell is in that specific State regardless of wether you should know
        # or not (for example, if a cell containing a Number is still Hidden, calling cell.is_number() will return True)
        #
        # Another way (prefered way) of getting a cell's state is by calling cell.get_state() which returns a State but will not tell
        # you the actual State (Number, Empty or Mine) unless the Cell's _visibility is Visible.
        # You can then compare this returned State to State.Hidden, State.Number, etc...
        #
        # The bottom line is "don't cheat"

        # Get surrounding cells
        # With a reference to a cell object
        cell = numbers[0]
        surrounding = board.get_surrounding(cell=cell)

        # With row and column indices
        (i, j) = board.get_cell_coord(cell)
        surrounding = board.get_surrounding(coord=(i, j))

        # Iterate through cells with an index
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                # the coordinates of 'cell' is the tuple (i, j)
                pass

        # About Flags
        # The Flag and Hidden States are considered different -> I may change this in the future
        # Trying to place a flag on a revealed Cell is considered an Error

        # Return Random Cell
        target = random.randint(min_value, max_value), random.randint(min_value, max_value)
        return target, False
