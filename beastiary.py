from fighter import Fighter


class Monster():
    def __init__(self,x,y,disp,color,name,description,blocks=True,ai_comp=None,fighter_comp=None):
        self.x = x
        self.y = y
        self.disp = disp
        self.color = color
        self.name = name
        self.description = description
        self.blocks = blocks
        self.ai_comp = ai_comp
        self.fighter_comp = fighter_comp

    def take_turn(self):
        if self.ai_comp: self.ai_comp.take_turn()

        else: return "The %s growls!" % (self.name)

    def get_damaged(self,attacker,damage):
        if self.fighter_comp:
            return self.fighter_comp.get_damaged(damage) #Will return the remaining HP

        else: return "The %s laughs at your pitiful attack!" % (self.name)

