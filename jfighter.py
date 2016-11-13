"""This file will eventually replace the current fighter.py class.
It's purpose is to implement a more interesting combat system.
The system will be based loosely on GURPS, DCSS, and other game systems I like.

Design notes:
1) Stats are as GURPS: ST, DX, IQ, HT
2) Some derived stats track with GURPS: Will, Per, FP
3) Other diverge, as listed below:
Basic Lift: Unlike GURPS, encumbrance starts at BLx10.

Basic Speed: # of actions that can be taken in 10 "seconds".
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
import attr
from random import randint, uniform

log = logging.getLogger(__name__)

@attr.s
class Skill():
    """Skills store advancement, handle success rolls, and track their level.
    Every player will have a "default" skill that is used for skills they don't
    have."""

    name = attr.ib()
    level = attr.ib()
    points = attr.ib()
    attribute = attr.ib()
    owner = attr.ib(owner)

    def skill_check(self,modifiers):
        target = (self.owner.stats[self.attribute]*5) + level + modifiers
        roll = randint(1,100)
        self.advance_check(target)
        return roll < target

    def advance_check(self,target):
        if target < 0: target = 0
        if target > 100: target = 100
        diff_mod = (-0.52 * target**2) + (5.1 * target) + 10
        points += (uniform(0.0,1.0) * diff_mod)

    def __repr__(self):
        return "%s (%s): %s (%04f)" % (self.name, self.attribute, self.level,
                                       self.points)

@attr.s
class Fighter():
    """Stats:
    ST, DX, IQ, HT, HP, Will, Per, FP, BL, BS, Skills
    stats is a dictionary with 'ST', 'DX', 'IQ', and 'HT' keys each with an int
    value."""
    stats = attr.ib() #Dictionary with {'ST':10,'DX':10,'IQ':10,'HT':10}
    max_hp = attr.ib()
    cur_hp = attr.ib()
    will = attr.ib()
    per = attr.ib()
    max_fp = attr.ib()
    cur_fp = attr.ib()
    bl = attr.ib()
    bs = attr.ib()
    speed = attr.ib()
    skills = attr.ib()

    def add_skill(self, skill, base_attribute, starting_level, starting_points):
        pass

