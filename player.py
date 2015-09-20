import pygame
import random

import creatures

from helpers import *

# base class for player
class Player(creatures.Creature):

    def __init__(self, (x,y)):
        creatures.Creature.__init__(self, (x,y))

        self.level = 1
        self.exp = 0
        self.gold = 0

    def generateStats(self):
    
        rem = 75 - (self.str+self.int+self.wis+self.con+self.dex+self.cha)
        for i in range(1,rem):
            v = random.randint(1,100)
            if v <= self.str_prob:
                self.str += 1
            elif v <= self.str_prob + self.int_prob:
                self.int += 1
            elif v <= self.str_prob + self.int_prob + self.wis_prob:
                self.wis += 1
            elif (v <= self.str_prob + self.int_prob + self.wis_prob +
                    self.dex_prob):
                self.dex += 1
            elif (v <= self.str_prob + self.int_prob + self.wis_prob +
                    self.dex_prob + self.con_prob):
                self.con += 1
            else:
                self.cha += 1
            # todo: implement stat maxes?


# nymph class
# very weak, low attack damage, but can steal items and stun
# (some?) wands, scrolls, potions automatically IDed
# starts with teleportitis
class Nymph(Player):

    def __init__(self, (x,y)):
        self.image = load_image("nymph.png",-1)
        # stats! kind of ugly, but what can we do...
        self.str = 6
        self.str_prob = 5
        self.int = 8
        self.int_prob = 30
        self.wis = 8
        self.wis_prob = 15
        self.dex = 10
        self.dex_prob = 15
        self.con = 8
        self.con_prob = 5
        self.cha = 14
        self.cha_prob = 30 # REM = 21
        self.hp = 7
        self.hp_gain = 6 # d6
        self.pow = 3

        # implement starting items!

        Player.__init__(self,((x,y)))

    def checkMove(self, x, y, tile_dict):

        # todo: implement wall-walking, etc
        if (x,y) in tile_dict:
            if tile_dict[(x,y)].nature == "floor":
                self.move(x,y)
        # otherwise, check fails and we don't move
