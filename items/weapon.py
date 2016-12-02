import item
import logging

log = logging.getLogger(__name__)

class Weapon(item.Item):

    def __init__(self, name, disp, color, game, effect, damage, dmg_type,
                 wielder, skill_name):
        item.Item(name, disp, color, game, effect, wielder)
        self.damage = damage
        self.dmg_type = damage_type
        self.skill_name = skill
