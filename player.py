from beastiary import Monster
from fighter import Fighter
directions = {"North":(-1,0), "South":(1,0), "East":(0,1), "West":(0,-1)}

class Player(Monster):
    def __init__(self,x,y,"@","Player",description="A stout warrior of courage and might",
                 blocks=True,fighter_comp(Fighter(10,4)):
        Monster.__init__(x,y,disp,color,description,blocks,fighter_comp)


