from random import uniform
from math import floor
import logging

log = logging.getLogger(__name__)

class Fighter():
    """Component required by all things which can take and cause damage."""

    def __init__(self,hp,atk):
        self.owner = None
        self.hp = hp
        self.current_hp = hp
        self.atk = atk

    def attack(self,target):     
        dmg = floor(self.atk * uniform(0.5,1,5))
        return target.take_damage(self.owner,dmg)

    def damaged(self,dmg):
        self.current_hp -= dmg
        return self.current_hp
