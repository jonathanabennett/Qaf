"""Base AI. This AI is what all the others inherit. It defines the things that
are common to all AIs."""
import logging

log = logging.getLogger(__name__)

class BaseAI():

    def __init__(self):
        self.visible = False
        self.state = "Aggressive"
        self.owner = False

    def check_neighbors(self, level):
        neighbors_addrs = level.get_neighbor_addrs(self.owner.x, self.owner.y)
        neighbors = [level.lookup(t[0],t[1]) for t in neighbors_addrs]
        return sorted(neighbors, key=lambda tile:tile.value)

    def take_turn(self, level):
        tile = level.lookup(self.owner.x, self.owner.y)
        if tile.value > self.owner.fighter_comp.stats['IQ']:
            return True

        if self.state == "Aggressive":
            log.debug("%s is taking turn." % (self.owner.name))
            adjacents = self.check_neighbors(level)
            log.debug("%s has %s neighbors." % (self.owner.name,
                                                len(adjacents)))
            finished = False
            while adjacents and not finished:
                log.debug("Inside decision loop.")
                dest = adjacents.pop(0)
                if dest.value == 0:
                    log.debug("The player! Attack him!")
                    self.owner.fighter_comp.attack(level.player)
                    break
                else:
                    if not dest.blocked:
                        log.debug("Checking if Tile %s, %s is closer." % (dest.x,
                                                                      dest.y))
                        if dest.value < tile.value:
                            log.debug("Tile %s, %s is closer!" % (dest.x,
                                                                  dest.y))
                            if self.owner.move_to(dest.x, dest.y, level):
                                finished = True
