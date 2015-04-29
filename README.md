# PythonMinesweeper
A Python 3.4 backend for a command-line minesweeper game and AI

Main.py : Initialize game and players and play game

Board   : the minesweeper grid and related methods
Cell    : represents on cell on the Board as well as the state of that cell
State   : Enum representing the different states a Cell can be in

Exceptions : Used to help the player spot potential errors and to relay messages between Board and Main

Bot     : the "interface" for an AI - just implement the get_move() method
RandomBot : AI that plays randomly, always

MinesweeperAi : code template for an AI. I've included a bunch of examples for how to use the Board and Cells
