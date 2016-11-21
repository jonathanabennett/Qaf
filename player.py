"""Defines a player. This will eventually hold all the creation factories for
the various classes."""
import logging
import beastiary
from jfighter import Fighter

log = logging.getLogger(__name__)

class Player(beastiary.Monster):
    """Players are controllable monsters. In theory, we could find a way to let
    multiple players exist in the game and take action in turn?"""
    def __init__(self, x, y, level,):
        beastiary.Monster.__init__(self, x=x, y=y, name="player", disp="@",
                         color="Player",
                         description="A hero of might and courage.",
                         level=level, blocks=True,
                                   fighter_comp=Fighter(st=10,dx=10,iq=10,ht=10))
