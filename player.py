"""Defines a player. This will eventually hold all the creation factories for
the various classes."""
import logging
from beastiary import Monster
from fighter import Fighter

log = logging.getLogger(__name__)
DIRECTIONS = {"North":(-1, 0), "South":(1, 0), "East":(0, 1), "West":(0, -1)}

class Player(Monster):
    """Players are controllable monsters. In theory, we could find a way to let
    multiple players exist in the game and take action in turn?"""
    def __init__(self, x, y, level,):
        Monster.__init__(self, x=x, y=y, name="player", disp="@",
                         color="Player",
                         description="A hero of might and courage.",
                         level=level, blocks=True, fighter_comp=Fighter(10,4))

