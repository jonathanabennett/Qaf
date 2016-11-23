"""Map and Tile Classes. This is the file where a lot of the display logic
happens."""
import sys
import uuid
import heapq
import logging
import beastiary

log = logging.getLogger(__name__)

class Tile:
    """The Tile Class defines a square on the map."""
    def __init__(self, blocked, x, y, block_sight=None):
        self.blocked = blocked

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

        if self.blocked: self.disp = "#"
        else: self.disp = "."

        self.value = sys.maxsize
        self.ident = uuid.uuid4()
        self.x = x
        self.y = y
        self.previous = None
        self.visited = False
        self.occupied = False

    def unblock(self, sight=False):
        """Function for deleting walls."""
        self.blocked = False
        self.block_sight = sight
        self.disp = '.'

    def block(self, sight=True):
        """Function for creating walls."""
        self.blocked = True
        self.block_sight = sight
        self.disp = '#'

    def __repr__(self):
        return self.disp

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.ident == other.ident
        else: return False

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.value < other.value
        else:
            return NotImplemented

    def __le__(self, other):
        if other.__class__ is self.__class__:
            return self.value <= other.value
        else: return NotImplemented

    def __gt__(self, other):
        if other.__class__ is self.__class__:
            return self.value > other.value
        else: return NotImplemented

    def __ge__(self, other):
        if other.__class__ is self.__class__:
            return self.value > other.value
        else: return NotImplemented

class Map:

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
        else: return Tile(True,x,y)

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
                    ret[y].append(self.lookup(x,y).value)
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
        for tile in self.grid.values():
            tile.value = sys.maxsize
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


if __name__ == "__main__":
    m = Map(10,10)
    ret = m.heatmap(6,6)
    pstr = ""
    for y in range(len(ret)):
        for x in range(len(ret[y])):
            pstr += str(ret[y][x])
        pstr += "\n"

    print(pstr)
