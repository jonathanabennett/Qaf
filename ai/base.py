"""Base AI. This AI is what all the others inherit. It defines the things that
are common to all AIs."""
import logging

log = logging.getLogger(__name__)

class BaseAI():

    def __init__(self):
        self.visible = False
        self.state = "Aggressive"
        self.owner = False

    def check_neighbors(self):
        neighbors_addrs = self.owner.level.get_neighbor_addrs(self.owner.x,
                                                              self.owner.y)
        neighbors = [self.owner.level.lookup(t[0],t[1]) for t in
                     neighbors_addrs]
        return sorted(neighbors, key=lambda tile:tile.value)

    def take_turn(self):
        tile = self.owner.level.lookup(self.owner.x, self.owner.y)
        if tile.value > 10:
            log.debug("Tile %s,%s is %s tiles away." %(tile.x, tile.y,
                                                       tile.value))
            return True
        if self.state == "Aggressive":
            log.debug("%s is taking turn." % (self.owner.name))
            adjacents = self.check_neighbors()
            log.debug("%s has %s neighbors." % (self.owner.name,
                                                len(adjacents)))
            finished = False
            while adjacents and not finished:
                log.debug("Inside decision loop.")
                dest = adjacents.pop(0)
                if dest.blocked:
                    log.debug("Tile %s, %s is blocked." % (dest.x, dest.y))
                    continue
                elif dest.value == 0:
                    log.debug("The player! Attack him!")
                    self.owner.fighter_comp.attack(self.owner.level.player)
                    self.finished = True
                elif not dest.blocked:
                    log.debug("Checking if Tile %s, %s is closer." % (dest.x,
                                                                      dest.y))
                    if dest.value <= tile.value:
                        log.debug("Tile %s, %s is closer!" % (dest.x, dest.y))
                        if self.owner.move_to(dest.x, dest.y):
                            finished = True
