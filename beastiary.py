from jfighter import Fighter
import logging
from uuid import uuid4
import maps

log = logging.getLogger(__name__)
DIRECTIONS = {"North":(0,-1), "NorthEast": (1,-1), "East":(1,0),
              "SouthEast":(1,1), "South":(0,1), "SouthWest":(-1,1),
              "West":(-1,0), "NorthWest":(-1,-1)}

class Monster():
    def __init__(self,x,y,disp,color,name,description,level,blocks=True,
                 ai_comp=None,fighter_comp=None):
        self.x = x
        self.y = y
        self.disp = disp
        self.color = color
        self.name = name
        self.description = description
        self.blocks = blocks
        self.ai_comp = ai_comp
        self.fighter_comp = fighter_comp
        self.level = level
        self.id = uuid4()
        if self.fighter_comp:
            if not self.fighter_comp.owner:
                self.fighter_comp.owner = self

    def take_turn(self):
        if self.level.lookup(self.x, self.y).value > 10:
            return False
        elif self.ai_comp: self.ai_comp.take_turn()

        else: return "The %s growls!" % (self.name)

    def get_damaged(self,attacker,damage):
        if self.fighter_comp:
            return self.fighter_comp.damaged(damage) #Will return the remaining HP

        else: return "The %s laughs at your pitiful attack!" % (self.name)

    def move_or_attack(self,direction):
        newX = self.x + DIRECTIONS[direction][0]
        newY = self.y + DIRECTIONS[direction][1]

        target = self.level.blocked(newX,newY)
        if not target:
            self.x = newX
            self.y = newY

        elif type(target) != type(maps.Tile):
            return self.fighter_comp.attack(target)
        else: return "Blocked by wall!"

    def get_speed(self):
        return self.fighter_comp.speed

    def died(self):
        self.disp = '%'
        self.blocks = False

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
