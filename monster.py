from jfighter import *
import logging
from uuid import uuid4
import maps
import ai

log = logging.getLogger(__name__)

DIRECTIONS = {"North":(0,-1), "NorthEast": (1,-1), "East":(1,0),
              "SouthEast":(1,1), "South":(0,1), "SouthWest":(-1,1),
              "West":(-1,0), "NorthWest":(-1,-1)}

class Monster():
    def __init__(self,x,y,disp,color,name,description,blocks=True,
                 ai_comp=None,fighter_comp=None, game=None):
        self.x = x
        self.y = y
        self.disp = disp
        self.color = color
        self.name = name
        self.description = description
        self.blocks = blocks
        self.ai_comp = ai_comp
        self.fighter_comp = fighter_comp
        self.game_instance = game
        self.id = uuid4()
        if self.fighter_comp:
            if not self.fighter_comp.owner:
                self.fighter_comp.owner = self
        if self.ai_comp:
            if not self.ai_comp.owner:
                self.ai_comp.owner = self

    def take_turn(self, level):
        if self.ai_comp:
            log.debug("Passing to %s's AI." % (self.name))
            self.ai_comp.take_turn(level)


    def get_damaged(self,attacker,damage):
        if self.fighter_comp:
            return self.fighter_comp.damaged(damage) #Will return the remaining HP

        else: return "The %s laughs at your pitiful attack!" % (self.name)

    def move_to(self, x, y, level):
        target = level.blocked(x,y)
        if not target:
            self.x = x
            self.y = y

    def move_or_attack(self,direction, level):
        newX = self.x + DIRECTIONS[direction][0]
        newY = self.y + DIRECTIONS[direction][1]

        target = level.blocked(newX,newY)
        if not target:
            self.x = newX
            self.y = newY
            self.fighter_comp.heal(uniform(0.0,0.2))

        elif isinstance(target, maps.Tile):
            return "blocked by wall!"
        else:
            self.fighter_comp.heal(uniform(0.0,0.2))
            return self.fighter_comp.attack(target)

    def get_speed(self):
        return self.fighter_comp.speed

    def died(self):
        self.disp = '%'
        self.blocks = False
        self.ai_comp = None
#        self.fighter_comp = None
        self.game_instance.add_message("%s has died." % (self.name))

    def __eq__(self,other):
        if self.id == other.id: return True
        else: return False

    def __ne__(self,other):
        if self.id != other.id: return True
        else: return False

    def __gt__(self,other):
        if self.id > other.id: return True
        else: return False

    def __ge__(self,other):
        if self.id >= other.id: return True
        else: return False

    def __lt__(self,other):
        if self.id < other.id: return True
        else: return False

    def __le__(self,ohter):
        if self.id <= other.id: return True
        else: return False

    def __str__(self):
        return "%s at %s, %s" % (self.name, self.x, self.y)

