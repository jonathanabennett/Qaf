import curses, sys
import logging
from math import floor

import beastiary
from player import Player
from maps import Map
from levelgen import MapGenerator

logging.basicConfig(filename="Qaf.log")
log = logging.getLogger(__name__)

directions = {"N":(-1,0), "S":(1,0), "E":(0,1), "W":(0,-1),
             "NW":(-1,-1), "NE":(-1,1), "SW":(1,-1), "SE":(1,1)}

class Game():
    """This is the master Object, coordinating everything. It is also what gets
    saved when we go to save the file."""
    def __init__(self, screen):
        self.main = screen
        curses.curs_set(0)
        self.main.scrollok(0)
        self.colorize()
        self.height, self.width = self.main.getmaxyx() 
        logging.debug(self.height)
        self.main.border(0)
        self.map_view = self.main.subwin(self.height-10,self.width-20,0,20)
        self.messages_view = self.main.subwin(self.height-10, 0)
        self.char_sheet = self.main.subwin(self.height-10, 20,0,0)
        self.player = Player(0,0,None)
        self.things = []
        self.map_height = 100
        self.map_width = 100
        if self.map_height < self.height-10: self.map_height = self.height-10
        if self.map_width < self.width-20: self.map_width = self.width - 20
        self.map = MapGenerator(self.map_width,self.map_height, self.things,self.player).map
        self.game_state = "playing"
        self.took_turn = False
        self.messages = []
        self.new_messages = ["Welcome to Qaf.",]
        self.keybindings = {ord("k"): {"function":self.player_move_attack,
                                       "args":{"direction":"N"}},
                            ord('j'): {"function":self.player_move_attack,
                                       "args":{"direction":"S"}},
                            ord('h'): {"function":self.player_move_attack,
                                       "args":{"direction":"W"}},
                            ord('l'): {"function":self.player_move_attack,
                                       "args":{"direction":"E"}},
                            ord('y'): {"function":self.player_move_attack,
                                       "args":{"direction":"NW"}},
                            ord('u'): {"function":self.player_move_attack,
                                       "args":{"direction":"NE"}},
                            ord('b'): {"function":self.player_move_attack,
                                       "args":{"direction":"SW"}},
                            ord('n'): {"function":self.player_move_attack,
                                       "args":{"direction":"SE"}},
                            ord('q'): {"function":self.save_game,
                                       "args":{"placeholder":0}}}
        self.main_loop()

    def colorize(self):
        curses.use_default_colors()
        curses.init_pair(1, 191, -1)
        curses.init_pair(2, -1, 250)
        curses.init_pair(3, -1, 235)
        curses.init_pair(4, 107, -1)
        curses.init_pair(5, 131, -1)
        self.color_palette = {}
        self.color_palette["Player"] = 0
        self.color_palette["NPC"] = 1
        self.color_palette["dark_wall"] = 2
        self.color_palette["dark_floor"] = 3
        self.color_palette["orc"] = 4
        self.color_palette["troll"] = 5

    def handle_messages(self):
        if self.new_messages:
            log.info(self.new_messages)
            self.new_messages.sort()
            disp = []
            old_msg = self.new_messages[0]
            msg_count = 0
            for message in self.new_messages:
                log.info(message)
                if message == old_msg:
                    msg_count += 1
                else:
                    if msg_count > 1:
                        disp.insert(0,"%s x%s" % (old_msg,msg_count))
                    else: disp.insert(0,old_msg)
                    old_msg = message
                    msg_count = 1
            disp.insert(0,old_msg)
            if len(disp) < self.messages_view.getmaxyx()[0]:
                log.info(disp)
                for line, message in enumerate(disp):
                    self.messages_view.addstr(line,1,message)
            if len(disp) > self.messages_view.getmaxyx()[0]:
                for line, message in enumerate(disp[-9:]):
                    self.messages_view.addstr(line,1,message)
                self.messages_view.addstr(10,1,"-more-")
                self.messages.extend(disp[:-9])
                del self.new_messages[:-9]

    def main_loop(self):
        while 1:
            self.render_all()
            self.took_turn = False

            c = self.main.getch()
            try:
                self.keybindings[c]["function"](**self.keybindings[c]["args"])
            except KeyError:
                continue
            if self.game_state == "playing" and self.took_turn == True:
                for thing in self.things:
                    if self.map.lookup(thing.x,thing.y).value < 10:
                        msg = thing.take_turn()
                        log.info(msg)
                        if msg: self.new_messages.append(msg)

    def look(self):
        """I want look to define a 'cursor' Thing. This thing will be added
        to the render list. While it is in the list, it takes precidence over player
        movements and gets to ignore calls to is_blocked when moving. Pressing
        'Enter' will cause the cursor to see what other objects have the same x and y
        coordinates and print them at the bottom of the screen. Then it will remove
        itself from the things list. """
        cursor = Thing(self.player.x,self.player.y, "X")
        self.things.insert(0, cursor)

    def player_move_attack(self, direction):
        """I chose to let the Game class handle redraws instead of objects.
        I did this because it will make it easier should I ever attempt to rewrite
        this with libtcod, pygcurses, or even some sort of browser-based thing.
        Display is cleanly separated from obects and map data.
        Objects use the variable name "thing" to avoid namespace collision."""
        curx = self.player.x
        cury = self.player.y
        newy = self.player.y + directions[direction][0]
        newx = self.player.x + directions[direction][1]
        blocked = self.is_blocked(newx,newy)
        if not blocked:
            log.debug("Not blocked")
            self.player.x = newx
            self.player.y = newy
            log.debug("Moved to %s,%s" % (self.player.x,self.player.y))
            self.took_turn = True
        else:
            for thing in self.things:
                if newx == thing.x and newy == thing.y:
                    self.new_messages.append(thing.get_attacked(self.player))
        return True

    def is_blocked(self, x, y):
        if self.map.lookup(x, y).blocked:
            log.info("Blocked by wall")
            return True

        for thing in self.things:
            if thing.blocks and x == thing.x and y == thing.y:
                log.info("Blocked by %s" % thing.description)
                return True
        return False

    def clear_thing(self, y, x, thing):
        """Broken out to handle stacks of things in one location, resurrecting
        things, and other times I don't want to just blit out the whole tile. Right
        now, it just blits the tile though..."""
        self.map_view.addch(y, x, " ",
                            curses.color_pair(self.color_palette["dark_floor"]))
        return True

    def render_all(self):
        self.map.heatmap(self.player.x,self.player.y,15)
        y_offset = floor((self.height-10)/2)
        x_offset = floor((self.width-20)/2)

        minY = self.player.y - y_offset
        maxY = self.player.y + y_offset
        if minY < 0: minY = 0
        if maxY > self.map.height: maxY = self.map.height
#The following code block tests whether we're too close to an edge and corrects for it
        if maxY-minY < self.height-10:
            if minY == 0: maxY = self.height-10
            else: minY = maxY - (self.height-10)

        minX = self.things[0].x - x_offset
        maxX = self.things[0].x + x_offset
        if minX < 0: minX = 0
        if maxX > self.map.width: maxX = self.map.width
        if maxX-minX < self.width-20:
            if minX == 0: maxX = self.width-20
            else: minX = maxX - (self.width-20)
        log.info("minX = %s, maxX = %s, minY = %s, maxY = %s" % (minX, maxX, minY, maxY))
        for y in range(minY,maxY):
            for x in range(minX,maxX):
                wall = self.map.lookup(x,y).blocked
                if wall:
                    try:
                        self.map_view.addch(y-minY, x-minX, " ",
                                            curses.color_pair(self.color_palette["dark_wall"]))
                    except curses.error: pass
                else:
                    try:
                        self.map_view.addch(y-minY, x-minX, " ",
                                            curses.color_pair(self.color_palette["dark_floor"]))
                    except curses.error: pass

        for thing in self.things:
            if minX <= thing.x <= maxX and minY <= thing.y <= maxY:
                self.draw_thing(thing, minX, minY)
        self.draw_thing(self.player, minX, minY)
        self.messages_view.box()
        self.char_sheet.box()
#        try:
#            self.messages_view.addstr(1,1,"Test Message")
#        except curses.error: pass
        self.handle_messages()
        try:
            self.char_sheet.addstr(1,1,"Character Sheet")
        except curses.error: pass
        self.map_view.refresh()
        self.messages_view.refresh()
        self.char_sheet.refresh()

    def draw_thing(self, thing, x_offset,y_offset):
        try:
          self.map_view.addch(thing.y-y_offset, thing.x-x_offset, thing.disp,
                              curses.color_pair(self.color_palette[thing.color]))
        except curses.error: pass

    def save_game(self,placeholder):
        sys.exit()

def loop(screen):
    g = Game(screen)

if __name__ == "__main__":
    curses.wrapper(loop) #Should I put the main loop outside the Game Object?
