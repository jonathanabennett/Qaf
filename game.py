import curses, sys
import logging
from math import floor

import beastiary
from player import Player
from maps import Map
from levelgen import MapGenerator

logging.basicConfig(filename="Qaf.log")
log = logging.getLogger(__name__)


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
        self.map_height = 100
        self.map_width = 100
        if self.map_height < self.height-10: self.map_height = self.height-10
        if self.map_width < self.width-20: self.map_width = self.width - 20
        self.current_level = MapGenerator(self.map_width,self.map_height,).map
        self.player = self.current_level.player
        self.game_state = "playing"
        self.took_turn = False
        self.messages = []
        self.new_messages = ["Welcome to Qaf.",]
        self.keybindings = {ord("k"): {"function":self.player.move_or_attack,
                                       "args":{"direction":"North"}},
                            ord('j'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"South"}},
                            ord('h'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"West"}},
                            ord('l'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"East"}},
                            ord('y'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"NorthWest"}},
                            ord('u'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"NorthEast"}},
                            ord('b'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"SouthWest"}},
                            ord('n'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"SouthEast"}},
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
            self.draw_screen()
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

    def clear_thing(self, y, x, thing):
        """Broken out to handle stacks of things in one location, resurrecting
        things, and other times I don't want to just blit out the whole tile. Right
        now, it just blits the tile though..."""
        self.map_view.addch(y, x, " ",
                            curses.color_pair(self.color_palette["dark_floor"]))
        return True

    def draw_screen(self):
        """This function will handle all screen renders. It takes a list of
        things and a grid (with is a list of lists of tiles. It will draw them
        all on the screen. The next step will be splitting out messaging and
        finally Character sheet display."""
        self.current_level.heatmap(self.player.x, self.player.y)
        x_offset = floor((self.width - 20) / 2)
        minX = self.player.x - x_offset
        maxX = self.player.x + x_offset - 1
        if minX < 0: minX = 0
        if maxX > self.current_level.width: maxX = self.current_level.width
        if maxX - minX < self.width - 20:
            if minX == 0: maxX = self.width-20
            else: minX = maxX - (self.width - 20)

        y_offset = floor((self.height - 10) / 2)
        minY = self.player.y - y_offset
        maxY = self.player.y + y_offset - 1
        if minY < 0: minY = 0
        if maxY > self.current_level.height: maxY = self.current_level.height
        if maxY - minY < self.height - 10:
            if minY == 0: maxY = self.height-10
            else: minY = maxY - (self.height-10)

        log.info("minX = %s, maxX = %s, minY = %s, maxY = %s" % (minX, maxX,
                                                                 minY, maxY))

        grid,things = self.current_level.full_render(minX,maxX,minY,maxY)

        #This has to be replaced with references to grid
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                wall = grid[y][x].blocked
                logging.info(wall)
                if wall:
                    try:
                        self.map_view.addch(y, x," ",
                                            curses.color_pair(self.color_palette["dark_wall"]))
                    except curses.error: pass
                else:
                    try:
                        self.map_view.addch(y,x," ",
                                            curses.color_pair(self.color_palette["dark_floor"]))
                    except curses.error: pass

        for thing in things:
            self.draw_thing(thing,minX,minY)
        self.draw_thing(self.player,minX,minY)
        self.messages_view.box()
        self.char_sheet.box()

        self.handle_messages()
        try: self.char_sheet.addstr(1,1,"Character Sheet")
        except curses.error: pass

        self.map_view.refresh()
        self.messages_view.refresh()

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
