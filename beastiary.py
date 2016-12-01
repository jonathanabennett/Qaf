from jfighter import Fighter
import logging
from random import randint
from ai import base
from monster import Monster

log = logging.getLogger(__name__)

ORC = {'st':0, 'dx':0, 'iq':-1, 'ht':2, 'disp':'o', 'color':'goblinoid',
       'name':'Orc', 'desc':'An Onery Orc'}

TROLL = {'st':8, 'dx':-3, 'iq':-4, 'ht':2, 'disp':'t', 'color':'troll',
         'name':'Troll', 'desc':'A Terrible Troll'}

ELF = {'st':-1, 'dx':1, 'iq':2, 'ht':0, 'disp':'e', 'color':'elf',
       'name':'Elf', 'desc':'An Elegant Elf'}

DWARF = {'st':1, 'dx':-1, 'iq':0, 'ht':1, 'disp':'d', 'color':'dwarf',
         'name':'Dwarf', 'desc':'A Determined Dwarf'}

HUMAN = {'st':0, 'dx':0, 'iq':0, 'ht':0, 'disp':'h', 'color':'human',
         'name':'Human', 'desc': 'A Hubristic Human'}

KOBOLD = {'st':-3, 'dx':4, 'iq':1, 'ht':-1, 'disp':'k', 'color':'goblinoid',
          'name':'Kobold', 'desc': 'A Quick Kobold'}

def create_monster(x,y,game,kind):
    st = randint(8 + kind['st'], 12 + kind['st'])
    dx = randint(8 + kind['dx'], 12 + kind['dx'])
    iq = randint(8 + kind['iq'], 12 + kind['iq'])
    ht = randint(8 + kind['ht'], 12 + kind['ht'])
    return Monster(x,y,kind['disp'],kind['color'],kind['name'], kind['desc'],
                   ai_comp=base.BaseAI(), fighter_comp=Fighter(st, dx, iq, ht),
                   game=game)
