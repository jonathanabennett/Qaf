import logging
from uuid import uuid4

log = logging.getLogger(__name__)

class Item():
    """Things which can be picked up and used. Currently, it only effects
    damage done and damage received. I hope to add attribute modification
    later."""

    def __init__(self, name, disp, color, game, effect, wielder):
        self.name = name
        self.disp = disp
        self.color = color
        self.game = game
        self.effect = effect
        self.wielder = wielder
        self.uuid = uuid4()
