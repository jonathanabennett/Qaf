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
            best_x, best_y = self.owner.vector_towards(level.player.x,
                                                       level.player.y)
            best_x += self.owner.x
            best_y += self.owner.y
            best_tile = level.lookup(best_x, best_y)
            move = self.owner.move_to(best_x, best_y, level)

            if isinstance(move, float):
                return move
            elif move:
                return True
            else:
                adjacents = self.check_neighbors(level)
                adjacents = [tile for tile in adjacents if not
                             tile.blocked]
                while adjacents:
                    dest = adjacents.pop(0)
                    if dest.value < tile.value:
                        if self.owner.move_to(dest.x, dest.y, level):
                            break
