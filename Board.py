__author__ = 'MagicalH4X'
import random
import Exceptions

from Cell import Cell
from State import State


class Board(tuple):

    def __new__(cls, *args, **kwargs):

        # Create Empty Grid
        size, mines = args[0], args[1]
        return super().__new__(cls, [tuple([Cell() for x in range(size)]) for y in range(size)])

    def __init__(self, size, mines):
        self._size = size
        self._mines = mines

        self.place_mines()
        self.set_number_cells()

    # Shows actual state of each Cell
    def reveal(self):

        # Column indices
        print("col".ljust(9, " "), end="")
        for index in range(self._size):
            print("{}".format(index).ljust(3, " "), end="")

        # Separator
        print("\n---------", end="")
        for index in range(self._size * 3):
            print("-", end="")
        print("")

        # Rows
        for index, row in enumerate(self):
            print("row {} |".ljust(9, " ").format(index), end="")
            for cell in row:
                if cell.is_mine():
                    print("*".center(3, " "), end="")
                elif cell.is_number():
                    print("{}".format(cell.value).center(3, " "), end="")
                else:
                    print("_".center(3, " "), end="")

            print("\n")

    # Print the board without revealing hidden state
    def show(self):

        # Column indices
        print("col".ljust(9, " "), end="")
        for index in range(self._size):
            print("{}".format(index).ljust(3, " "), end="")

        # Separator
        print("\n---------", end="")
        for index in range(self._size * 3):
            print("-", end="")
        print("")

        for index, row in enumerate(self):
            print("row {} |".ljust(9, " ").format(index), end="")
            for cell in row:
                if cell.is_visible():
                    if cell.is_mine():
                        print("*".center(3, " "), end="")
                    elif cell.is_number():
                        print("{}".format(cell.value).center(3, " "), end="")
                    else:
                        print("_".center(3, " "), end="")
                elif cell.has_flag():
                    # Unicode flag
                    print(u"\u2691".center(3, " "), end="")
                else:
                    # Unicode square
                    print(u"\u2395".center(3, " "), end="")

            print("\n")

    # Get list of surrounding cells
    #
    # @param cell : instance of Cell
    # @param coord : tuple of form (i,j)
    # @return list(Cell)
    # Note : pass either cell or coord parameter. passing coord will be faster ( O(1) )
    #
    # Example board.get_surrounding(cell=my_cell) or board.get_surrounding(my_cell)
    # Example board.get_surrounding(coord=(0,2))
    def get_surrounding(self, cell=None, coord=None):

        if cell is not None:
            coord = self.get_cell_coord(cell)

        i, j = coord
        adjacent_cells = (
            # TopLeft, Top, TopRight
            (i - 1, j - 1), (i, j - 1), (i + 1, j - 1),
            # Left, Right
            (i - 1, j), (i + 1, j),
            # BottomLeft, Bottom, BottomRight
            (i - 1, j + 1), (i, j + 1), (i + 1, j + 1)
        )

        return [self[x][y] for (x, y) in adjacent_cells if
                0 <= y < self._size and 0 <= x < self._size]

    # Get (i,j) coordinate tuple for cell 'c'
    def get_cell_coord(self, c):

        for i, col in enumerate(self):
            for j, cell in enumerate(col):
                if cell is c:
                    return i, j
        return None

    def is_solved(self):
        # If there are exactly 0 cells which are not mines that are still hidden ( State.Hidden or State.Flag )
        return len([self[i][j] for i in range(self._size) for j in range(self._size) if not self[i][j].is_mine() and not self[i][j].is_visible()]) == 0

    # Set the state and value of all non-mine cells to represent the number of mines around it
    # 0 mines = State.Empty
    # > 0 mines = State.Number and value is set accordingly
    def set_number_cells(self):

        for i, col in enumerate(self):
            for j, cell in enumerate(col):
                if not cell.is_mine():
                    surrounding = self.get_surrounding(coord=(i, j))
                    adj_mines = len([cell for cell in surrounding if cell.is_mine()])
                    cell.state = State.Number if adj_mines > 0 else State.Empty
                    cell.value = adj_mines if adj_mines > 0 else None

    # Places randomized mines on an empty board
    def place_mines(self):

        # List All Possible Coordinate Tuples (x,y)
        coordinates = [(x, y) for x in range(self._size) for y in range(self._size)]

        # Place Mines
        for n in range(self._mines):
            index = random.randint(0, len(coordinates)-1)
            i, j = coordinates.pop(index)
            self[i][j].state = State.Mine

    # Moves a single mine to another non-mine cell
    # Used when player selects a mine on first turn (caus c'mon, that's not cool)
    def move_mine(self, target):

        # Get all Empty and Number cells other than the one being moved
        candidates = [cell for row in self for cell in row if (cell is not target) and (not cell.is_mine())]

        # Choose one randomly
        destination = candidates[random.randint(0, len(candidates)-1)]

        # Move Mine
        target.state = State.Empty
        target.value = None

        destination.state = State.Mine
        destination.value = None

    # Toggles state of cell from/to Hidden and Flag
    def toggle_flag(self, cell):
        cell.state = State.Flag if cell.state == State.Hidden else State.Hidden

    # Applies a player action
    # @param <Cell|tuple> target : either a Cell instance or a tuple of form (row, column)
    #
    # @action : toggle flag on target (flag=True)
    # @action : reveal target (flag=False)
    #
    # If this is the first turn and the player selects a mine, we move that mine to another
    # cell and recalculate the Number cells
    def player_action(self, target, flag=False, first_move=False):

        # If target is a tuple get the corresponding Cell
        if isinstance(target, tuple):
            i, j = target

            # Check that given indices are valid for board of size self._size
            if (not 0 <= i < self._size) or (not 0 <= j < self._size):
                message = "Board.player_actions() Error : Coordinates ({}, {}) invalid for board of size {}".format(i, j, self._size)
                raise Exceptions.IndicesOutOfBoundsException(message)

            # Get Cell object
            target = self[i][j]

        # Toggle Flag
        if flag:
            if target.is_visible():
                message = "Board.player_actions() Error : Cannot place flag on revealed cell"
                raise Exceptions.InvalidFlagTarget(message)

            self.toggle_flag(target)

        # Reveal selected cell
        else:
            # If it's the first move and player selected a mine
            # 1. Move mine
            # 2. Recalculate Number Cells
            if first_move and target.is_mine():
                try:
                    self.move_mine_from_perimeter(target, target)
                except Exceptions.NoPossibleMoveDestinationException:
                    self.move_mine(target)

                self.set_number_cells()

            # If it's the first move and player selects a Number cell
            # 1. Move all surrounding mines
            # 2. Recalculate Number Cells
            elif first_move and target.is_number():
                adj_mines = [cell for cell in self.get_surrounding(cell=target) if cell.is_mine()]
                for mine in adj_mines:
                    try:
                        self.move_mine_from_perimeter(target, mine)
                    except Exceptions.NoPossibleMoveDestinationException:
                        self.move_mine(mine)
                self.set_number_cells()

            # Reveal the cell
            if target.is_mine():
                raise Exceptions.YouBlewUp("BOOOOOOMMMM!!! You hit a mine - Game Over :(")

            elif target.is_number():
                target.visibility = State.Visible
            else:
                self.reveal_cell(self.get_cell_coord(target), [])

    # Moves mine Cell to a new destination not in the perimeter of origin
    # If this is not possible an exception is raised
    def move_mine_from_perimeter(self, origin, mine):
        i, j = self.get_cell_coord(origin)
        invalid_destinations = (
            (i, j),
            (i-1, j), (i+1, j), (i, j-1), (i, j+1),
            (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)
        )
        candidates = [self[x][y] for x in range(self._size) for y in range(self._size)
                      if (x, y) not in invalid_destinations
                      and (not self[x][y].is_mine())]

        if len(candidates) == 0:
            raise Exceptions.NoPossibleMoveDestinationException()

        destination = candidates[random.randint(0, len(candidates)-1)]

        # Move Mine
        mine.state = State.Empty
        mine.value = None

        destination.state = State.Mine
        destination.value = None


    # Reveal Empty Cell at given coordinates and recursively reveal adjacent Number and Empty cells
    def reveal_cell(self, coord, queue):
        i, j = coord
        cell = self[i][j]

        # Reveal Cell
        cell.visibility = State.Visible
        hidden_adj = self.get_adjacent_hidden_coord(coord)

        for adj_coord in hidden_adj:
            x, y = adj_coord

            # Reveal adjacent Number cells
            if self[x][y].is_number():
                self[x][y].visibility = State.Visible

            # Queue up empty cells for recursive call
            elif self[x][y].is_empty():
                queue.append(adj_coord)

        if len(queue) > 0:
            self.reveal_cell(queue.pop(), queue)

    # Returns list of adjacent cells (left, right, top and bottom) which are Hidden as coordinate tuples
    # Used to reveal an area of the board when an empty cell is selected
    def get_adjacent_hidden_coord(self, coord):
        i, j = coord
        adjacent = (
            (i, j-1), (i, j+1), (i-1, j), (i+1, j),
            (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)
        )

        return [(x, y) for (x, y) in adjacent
                if 0 <= x < self._size
                and 0 <= y < self._size
                and self[x][y].is_hidden()]
