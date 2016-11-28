from jfighter import Fighter
import logging
from uuid import uuid4
import maps
from random import randint, uniform
from ai import base
from monster import Monster

log = logging.getLogger(__name__)

def create_orc(x,y, game):
    st = randint(8,12)
    dx = randint(8,11)
    iq = randint(6,10)
    ht = randint(9,13)
    fgt_comp = Fighter(st,dx,iq,ht)
    ai_comp = base.BaseAI()
    ret = Monster(x,y,'o','orc','Orc','An Onery Orc', game=game,
                  fighter_comp=fgt_comp, ai_comp=ai_comp)
    return ret

def create_troll(x,y, game):
    st = randint(12,16)
    dx = randint(6,10)
    iq = randint(4,8)
    ht = randint(10,14)
    ai_comp = base.BaseAI()
    fgt_comp = Fighter(st,dx,iq,ht)
    return Monster(x,y,'T','troll','Troll','A Terrible Troll', game=game,
                   fighter_comp = fgt_comp, ai_comp=ai_comp)
