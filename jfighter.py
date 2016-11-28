"""This file will eventually replace the current fighter.py class.
It's purpose is to implement a more interesting combat system.
The system will be based loosely on GURPS, DCSS, and other game systems I like.

Design notes:
1) Stats are as GURPS: ST, DX, IQ, HT
2) Some derived stats track with GURPS: Will, Per, FP
3) Other diverge, as listed below:
Basic Lift: Unlike GURPS, encumbrance starts at BLx10.

Basic Speed: # of actions that can be taken in 5 "seconds".
    This means I need to re-write the main loop in game.py. The easiest way will be
turning things into a heapq where each entry is (time,thing). Then I just pop things
off the heap, take their action, calc their next turn, and add them back to the heap.
When the character's turn arrives, advances pause until the player's turn is finished.

HP: HP is an injury threshold for a Wounding system, not an count-down timer to death.

4) Implementation questions
Damage: The wounding system needs to be designed.

Skill rolls: Will I transliterate the GURPS roll-under tests or will I use a straight percentile
system?

CP: Instead of descrete CP, I want skills to slowly accure up to their next level, taking longer to
    advance for each additional level. Perhaps some sort of exponential or logarithmic curve between
    level? This requires some hardcore mathing.

Magic: How to handle this? This will be an important sticking point. Research G:Magic, G:Magic
    Styles, and G:T for ideas

Advantages: Modified GURPS style? Needs serious design work."""

import logging
from random import randint, uniform

log = logging.getLogger(__name__)

class Skill():
    """Skills store advancement, handle success rolls, and track their level.
    Every player will have a "default" skill that is used for skills they don't
    have."""

    def __init__(self, name, level, points, attribute, owner):
        """Name = The name of the skill, string
        level = the current skill level, a percentage
        points = the points towards the next skill level
        attribute = a string, must match ST, DX, IQ, or HT
        owner = The fighter object which owns this skill."""
        self.name = name
        self.level = level
        self.points = points
        self.attribute = attribute
        self.owner = owner

    def skill_check(self,modifiers):
        target = (self.owner.stats[self.attribute]*5) + self.level + modifiers
        roll = randint(1,100)
        self.advance_check(target)
        return roll < target

    def advance_check(self,target):
        if target < 0: target = 0
        if target > 100: target = 100
        diff_mod = (-0.52 * target**2) + (5.1 * target) + 10
        if diff_mod < 0: diff_mod = 0.1
        self.points += (uniform(0.0,1.0) * diff_mod)
        while self.points >= self.level+1:
            self.level += 1
            self.points -= self.level

    def __repr__(self):
        return "%s (%s): %s (%04f)" % (self.name, self.attribute, self.level,
                                       self.points)

class Fighter():
    """Stats:
    ST, DX, IQ, HT, HP, Will, Per, FP, BL, BS, Skills
    stats is a dictionary with 'ST', 'DX', 'IQ', and 'HT' keys each with an int
    value."""

    def __init__(self, st=10, dx=10, iq=10, ht=10, max_hp=False, cur_hp=False,
                 will=False, per=False, max_fp=False, cur_fp=False, bl=False,
                 bs=False, speed=False, skills={}, owner=False):
        self.stats = {'ST':st, 'DX':dx, 'IQ':iq, 'HT':ht}

        self.max_hp = max_hp
        if not self.max_hp: self.max_hp = self.stats['ST']

        self.cur_hp = cur_hp
        if not cur_hp: self.cur_hp = self.max_hp

        self.will = will
        if not self.will: self.will = self.stats['IQ']

        self.per = per
        if not self.per: self.per = self.stats['IQ']

        self.max_fp = max_fp
        if not self.max_fp: self.max_fp = self.stats['HT']

        self.cur_fp = cur_fp
        if not self.cur_fp: self.cur_fp = self.max_fp

        self.bl = bl
        if not self.bl: self.bl = self.stats['ST'] * self.stats['ST'] / 5

        self.bs = bs
        if not self.bs: self.bs = (self.stats['DX'] + self.stats['HT']) / 4.0

        self.speed = speed
        if not self.speed: self.speed = self.bs/5.0

        self.skills = skills
        self.owner = False

    def add_skill(self, skillname, base_attribute, starting_level, starting_points):
        self.skills[skillname] = Skill(skillname, float(starting_level),
                                       float(starting_points), base_attribute,
                                       self)

    def attack(self, target):
        try:
            sk = self.skills["Attack"]
        except:
            self.add_skill("Attack", 'ST', 0, 0)
        dmg = 0
        if self.skills["Attack"].skill_check(0):
            dmg = self.roll_dmg()
        return target.get_damaged(self.owner, dmg)

    def roll_dmg(self):
        return (self.stats['ST'] * uniform(0.5,1.5))/10.0

    def damaged(self,dmg):
        self.cur_hp -= dmg
        if self.cur_hp < 0:
            self.owner.died()
        return self.cur_hp

    def heal(self,amount):
        self.cur_hp += amount
        if self.cur_hp > self.max_hp: self.cur_hp = self.max_hp
