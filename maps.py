import sys
import uuid
from time import process_time
import heapq

class Tile:
    
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

    def unblock(self,sight=False):
        self.blocked = False
        self.block_sight = sight
        self.disp = '.'

    def block(self,sight=True):
        self.blocked = True
        self.block_sight = sight
        self.disp = '#'
    
    def __repr__(self):
        return self.disp

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.ident == other.ident
        else: return False

    def __ne__(self,other):
        result = self.__eq__(other)
        return not result

    def __lt__(self,other):
        if other.__class__ is self.__class__:
            return self.value < other.value
        else:
            return NotImplemented

    def __le__(self,other):
        if other.__class__ is self.__class__:
            return self.value <= other.value
        else: return NotImplemented

    def __gt__(self,other):
        if other.__class__ is self.__class__:
            return self.value > other.value
        else: return NotImplemented

    def __ge__(self,other):
        if other.__class__ is self.__class__:
            return self.value > other.value
        else: return NotImplemented
        
class Map:
    
    def __init__(self, maxx, maxy):
        self.width = maxx
        self.height = maxy
        self.grid = {}
        for x in range(self.width):
            for y in range(self.height):
                self.grid[(x,y)] = Tile(True,x,y)

    def lookup(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[(x,y)]
        else: return False

    def get_neighbor_addrs(self, x, y):
        ret = []
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                ret.append((i,j))
        return ret
 
    def __repr__(self):
        ret = ""
        for y in range(self.height):
            for x in range(self.width):
                ret += str(self.lookup(x,y))
            ret += '\n'
        return ret

    def render(self, minX, maxX, minY, maxY):
        ret = []
        if minX < 0: minX = 0
        if minY < 0: minY = 0
        if maxX > self.width: maxX = self.width
        if maxY > self.height: maxY = self.height
        for y in range (minY,maxY):
            ret.append([])
            for x in range(minX,maxX):
                ret[y].append(self.lookup(x,y))
        return ret
        
    def heatmap(self, source_x,source_y,max_dist=15):
        for tile in self.grid.values():
            tile.value = sys.maxsize
        l_open = []
        source = self.lookup(source_x,source_y)
        if source: l_open.append((0,source,source)) #(value,cell,previous)
        
        while l_open:
            value,cell,previous = heapq.heappop(l_open)
            if cell.visited or value > max_dist: continue
            cell.visited = True
            cell.previous = previous
            cell.value = value
            for x,y in self.get_neighbor_addrs(cell.x,cell.y):
                c = self.lookup(x,y)
                if c and not (c.visited or c.blocked):
                    heapq.heappush(l_open, (value+1, c, cell))

        return self.render(0,self.width, 0,self.height)
                                

if __name__ == "__main__":
    m = Map(40,30)
    for x in range(1,7):
        for y in range (1,10):
            m.lookup(x,y).blocked = False
    print(m.heatmap(6,6))
