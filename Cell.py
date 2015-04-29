__author__ = 'cthulhu'
from State import State


# Cell
# @property _state : the actual hidden State of a cell ( Mine | Empty | Number )
#       getter : cell.state
#       setter : cell.state = State.Empty
#
# @property _value : if state is Number , represents the number value for the cell,
#   ie. the number of surrounding mines ( ignored if state is Mine or Empty - value should then be None )
#       getter : cell.value
#       setter : cell.value = None
#
# @property _visibility : the visible state of the cell ( Hidden | Visible | Flag )
#       getter : cell.visibility
#       setter : cell.visibility = State.Hidden
#
#
class Cell:

    def __init__(self, state=State.Empty, value=None, visibility=State.Hidden):
        self._state = state
        self._value = value
        self._visibility = visibility

    # Cell.state
    # getter : cell.state
    # setter : cell.state = State.Empty
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    # Cell.value
    # getter : cell.value
    # setter : cell.value = None
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    # Cell.visibility
    # getter : cell.visibility
    # setter : cell.visibility = State.Hidden
    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        self._visibility = visibility

    # Convenience Methods for Board class
    def is_mine(self):
        return self._state == State.Mine

    def is_empty(self):
        return self._state == State.Empty

    def is_number(self):
        return self._state == State.Number

    def has_flag(self):
        return self.visibility == State.Flag

    def is_hidden(self):
        return self.visibility == State.Hidden

    def is_visible(self):
        return self.visibility == State.Visible

    # For use by Bots
    def get_state(self):
        if self.visibility != State.Visible:
            return self.visibility
        else:
            return self._state
