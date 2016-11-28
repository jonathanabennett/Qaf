import curses, sys
import logging
import heapq
from math import floor
import beastiary
from player import Player
from maps import Map
from levelgen import MapGenerator
from messages import MessageWindow, Message
from charsheet import CharSheet

logging.basicConfig(filename="Qaf.log", level=logging.DEBUG)

class Game():
    """This is the master Object, coordinating everything. It is also what gets
    saved when we go to save the file."""
    def __init__(self, screen):
        self.main = screen
        curses.curs_set(0)
        self.main.scrollok(0)
        self.colorize()
        self.height, self.width = self.main.getmaxyx()
        self.main.border(0)
        self.map_view = self.main.subwin(self.height-10,self.width-20,0,20)
        self.messages_view = self.main.subwin(self.height-10, 0)
        self.msg_handler = MessageWindow(window=self.messages_view,
                                         message_list=[])
        self.char_sheet = self.main.subwin(self.height-10, 20,0,0)
        self.map_height = 100
        self.map_width = 100
        if self.map_height < self.height-10: self.map_height = self.height-10
        if self.map_width < self.width-20: self.map_width = self.width - 20
        self.current_level = MapGenerator(self.map_width,self.map_height,self).map
        self.player = self.current_level.player
        self.char_sheet = CharSheet(self.char_sheet, self.player)
        self.event_queue = []
        self.timer = 0.0
        heapq.heappush(self.event_queue, (0.0, self.player))
        self.populate_events()
        self.game_state = "playing"
        self.took_turn = False
        self.msg_handler.new_message(Message(0.0,"Welcome to Qaf."))
        self.keybindings = {ord("k"): {"function":self.player.move_or_attack,
                                       "args":{"direction":"North",
                                               "level": self.current_level}},
                            ord('j'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"South",
                                               "level": self.current_level}},
                            ord('h'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"West",
                                               "level": self.current_level}},
                            ord('l'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"East",
                                               "level": self.current_level}},
                            ord('y'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"NorthWest",
                                               "level": self.current_level}},
                            ord('u'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"NorthEast",
                                               "level": self.current_level}},
                            ord('b'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"SouthWest",
                                               "level": self.current_level}},
                            ord('n'): {"function":self.player.move_or_attack,
                                       "args":{"direction":"SouthEast",
                                               "level": self.current_level}},
                            ord('s'): {"function":self.player.rest,
                                       "args": {}},
                            ord('q'): {"function":self.save_game,
                                       "args":{"placeholder":0}}}
        self.main_loop()

    def populate_events(self):
        for thing in self.current_level.things:
            self.add_event(thing)
        return True

    def add_event(self,event):
        heapq.heappush(self.event_queue, (self.timer + event.get_speed(), event))
        return True

    def remove_event(self, event):
        pass

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

    def main_loop(self):
        while 1:
            self.took_turn = False
            self.timer, next_actor = heapq.heappop(self.event_queue)
            if isinstance(next_actor, Player):
                self.draw_screen()
                c = self.main.getch()
                try:
                    msg = self.keybindings[c]["function"](**self.keybindings[c]["args"])
                    if msg:
                        self.add_message(msg)
                    self.add_event(next_actor)
                    self.current_level.heatmap(self.player.x, self.player.y)
                except KeyError: continue
            else:
                msg = next_actor.take_turn(self.current_level)
                if msg:
                    if msg == "Game over.":
                        self.save_game()
                    self.msg_handler.new_message(Message(msg))
                self.add_event(next_actor)

    def add_message(self, text):
        self.msg_handler.new_message(Message(self.timer, text))

    def look(self):
        """I want look to define a 'cursor' Thing. This thing will be added
        to the render list. While it is in the list, it takes precidence over player
        movements and gets to ignore calls to is_blocked when moving. Pressing
        'Enter' will cause the cursor to see what other objects have the same x and y
        coordinates and print them at the bottom of the screen. Then it will remove
        itself from the things list. """
        cursor = Thing(self.player.x,self.player.y, "X")
        self.things.insert(0, cursor)
        return True

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

        logging.info("minX = %s, maxX = %s, minY = %s, maxY = %s" % (minX, maxX,
                                                                 minY, maxY))

        grid,things = self.current_level.full_render(minX,maxX,minY,maxY)

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                wall = grid[y][x].blocked
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
#            logging.debug(str(thing))
            self.draw_thing(thing,minX,minY)
        self.draw_thing(self.player,minX,minY)

        self.msg_handler.update_messages()
        self.char_sheet.update_sheet()

        self.map_view.refresh()

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
