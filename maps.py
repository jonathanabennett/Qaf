"""Map and Tile Classes. This is the file where a lot of the display logic
happens."""
import sys
import uuid
import heapq
import logging
from tile import Tile

log = logging.getLogger(__name__)

class Level:

    def __init__(self, maxx, maxy, grid={}, things=[]):
        self.width = maxx
        self.height = maxy
        self.grid = grid
        self.things = things
        self.player = None
        for x in range(self.width):
            for y in range(self.height):
                self.grid[(x,y)] = Tile(True,x,y)

    def lookup(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[(x,y)]
        else:
            log.debug("Not a real tile.")
            return Tile(True,x,y)

    def get_neighbor_addrs(self, x, y):
        ret = []
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                ret.append((i,j))
        return ret

    def add_monster(self, monster):
        self.things.append(monster)

    def blocked(self,x,y):
        if self.lookup(x,y).blocked:
            return self.lookup(x,y)
        else:
            for thing in self.things:
                if thing.x == x and thing.y == y and thing.blocks:
                    return thing
            return False

    def __repr__(self):
        ret = ""
        for y in range(self.height):
            for x in range(self.width):
                ret += str(self.lookup(x,y))
            ret += '\n'
        return ret

    def render(self, minX, maxX, minY, maxY,heatp=False):
        ret = []
        if minX < 0: minX = 0
        if minY < 0: minY = 0
        if maxX > self.width: maxX = self.width
        if maxY > self.height: maxY = self.height
        if not heatp:
            for y in range (minY,maxY):
                ret.append([])
                for x in range(minX,maxX):
                    ret[y].append(self.lookup(x,y))
        else:
            for y in range(minY,maxY):
                ret.append([])
                for x in range(minX,maxX):
                    if self.lookup(x,y).value == sys.maxsize:
                        ret[y].append("#")
                    else: ret[y].append(self.lookup(x,y).value)
        return ret

    def full_render(self, minX, maxX, minY, maxY, heatp=False):
        map_ret = []

        if not heatp:
            for y in range(0, maxY-minY):
                map_ret.append([])
                for x in range(minX,maxX):
                    map_ret[y].append(self.lookup(x,minY+y))

        thing_ret = []
        for thing in self.things:
            if minX <= thing.x <= maxX:
                if minY <= thing.y <= maxY:
                    thing_ret.append(thing)

        return (map_ret, thing_ret)

    def heatmap(self, source_x,source_y):
        log.debug("Updating Heatmap.")
        for tile in self.grid.values():
            tile.value = sys.maxsize
            tile.previous = None
            tile.visited = False
        l_open = []
        source = self.lookup(source_x,source_y)
        if source: l_open.append((0,source,source)) #(value,cell,previous)

        while l_open:
            value,cell,previous = heapq.heappop(l_open)
            if cell.visited: continue
            cell.visited = True
            cell.previous = previous
            cell.value = value
            for x,y in self.get_neighbor_addrs(cell.x,cell.y):
                c = self.lookup(x,y)
                if c and not (c.visited or c.blocked):
                    heapq.heappush(l_open, (value+1, c, cell))

        return self.render(0,self.width, 0,self.height,heatp=True)

    def print_heatmap(self):
        ret = ""
        for y in range(self.height):
            for x in range(self.width):
                ret += "%2d" % (self.grid[(x,y)]).value
            ret += "\n"
        return ret


if __name__ == "__main__":
    m = Map(50,50)
    for tile in m.grid.values():
        tile.unblock()
    m.heatmap(6,6)
    print(m.print_heatmap())
    m.heatmap(10,10)
    print(m.print_heatmap())
