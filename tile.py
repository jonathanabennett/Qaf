import uuid
import sys

class Tile:
    """The Tile Class defines a square on the map."""
    def __init__(self, blocked, x, y, block_sight=None):
        self.blocked = blocked

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

        if self.blocked: self.disp = "#"
        else: self.disp = "."

        self.value = sys.maxsize
        self.ident = uuid.uuid4()
        self.x = x
        self.y = y
        self.previous = None
        self.visited = False
        self.occupied = False

    def unblock(self, sight=False):
        """Function for deleting walls."""
        self.blocked = False
        self.block_sight = sight
        self.disp = '.'

    def block(self, sight=True):
        """Function for creating walls."""
        self.blocked = True
        self.block_sight = sight
        self.disp = '#'

    def __repr__(self):
        return self.disp

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.ident == other.ident
        else: return False

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.value < other.value
        else:
            return NotImplemented

    def __le__(self, other):
        if other.__class__ is self.__class__:
            return self.value <= other.value
        else: return NotImplemented

    def __gt__(self, other):
        if other.__class__ is self.__class__:
            return self.value > other.value
        else: return NotImplemented

    def __ge__(self, other):
        if other.__class__ is self.__class__:
            return self.value > other.value
        else: return NotImplemented

