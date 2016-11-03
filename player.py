from beastiary import Monster
from fighter import Fighter
directions = {"North":(-1,0), "South":(1,0), "East":(0,1), "West":(0,-1)}

class Player(Monster):
    def __init__(self,x,y,level,):
        Monster.__init__(self,x=x,y=y,name="player",disp="@",color="Player",
                        description="A hero of might and courage.",
                        level=level,blocks=True,fighter_comp=Fighter(10,4))


