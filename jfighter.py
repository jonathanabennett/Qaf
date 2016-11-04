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

Skill rolls: Will I transliterate the GURPS roll-under tests or will I use a straight percentile system?

CP: Instead of descrete CP, I want skills to slowly accure up to their next level, taking longer to
    advance for each additional level. Perhaps some sort of exponential or logarithmic curve between levels?
    This requires some hardcore mathing.

Magic: How to handle this? This will be an important sticking point. Research G:Magic, G:Magic Styles, and G:T for ideas

Advantages: Modified GURPS style? Needs serious design work."""
import attr
import logging

log = logging.getLogger(__name__)

@attr.s
class Fighter():

        """Stats:
ST, DX, IQ, HT, HP, Will, Per, FP, BL, BS, Skills"""
