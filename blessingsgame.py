from blessings import Terminal
from maps import Map
from levelgen import MapGenerator
from thing import Thing
from player import Player
import logging
import beastiary
from math import floor

logging.basicConfig(filename="game.log", level=logging.DEBUG)

class Game():

    def __init__(self, save=False):
    
        self.term = Terminal()
        self.term.enterfullscreen()
        self.screen_resize()
        self.things = []
        self.things.append(Player(int(floor(self.map_width/2)),
                                  int(floor(self.map_height/2))))
        self.cur_level = MapGenerator(self.map_width, self.map_height,
                                      self.things).map
        self.game_state = "playing"
        self.keybindings = {}
        self.main_loop()

    def screen_resize(self):
        #Dynamically resize map
        self.map_height = self.term.height - 1
        self.map_width = self.term.width - 20 #Sets width of map.

    def main_loop(self):
        disp = ""   
        level = self.cur_level.render(0,self.map_width,0,self.map_height)
        for y in range(self.term.height):
            if y == self.term.height-1:
                disp += "Message Area"
            else:
                disp += "  Character  Sheet  "
                for i,x in enumerate(level[y]):
                    disp += str(x)
                disp += "\n"

        print(disp)
        with self.term.location():
            for thing in self.things:
                print(self.term.move(thing.x + 20,thing.y) + thing.disp)
        input()
        self.term.exitfullscreen()
        import sys
        sys.exit()

if __name__ == "__main__":
    g = Game()
