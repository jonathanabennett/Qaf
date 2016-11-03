from random import uniform
from math import floor

class Fighter():
    """Component required by all things which can take and cause damage."""

    def __init__(self,owner,hp,atk):
        self.owner = owner
        self.hp = hp
        self.current_hp = hp
        self.atk = atk

    def attack(self,target):
        dmg = floor(self.atk * uniform(0.5,1,5))
        return target.take_damage(self.owner,dmg)

    def damaged(self,dmg):
        self.current_hp -= dmg
        return self.current_hp
