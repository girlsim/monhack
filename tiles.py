import pygame

from helpers import *

class Tile(pygame.sprite.Sprite):

    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        # WARNING! ASSUMES TILESIZE OF 18x18!
        x,y = coords
        self.rect = self.image.get_rect()
        self.rect.center = (x*18+9, y*18+9)
        self.coords = coords

class WallCorner(Tile):

    def __init__(self, coords):
        self.image = load_image("corner.png")
        self.nature = "wall"
        Tile.__init__(self, coords)

class WallLR(Tile):

    def __init__(self, coords):
        self.image = load_image("lr.png")
        self.nature = "wall"
        Tile.__init__(self, coords)

class WallUD(Tile):

    def __init__(self, coords):
        self.image = load_image("ud.png")
        self.nature = "wall"
        Tile.__init__(self, coords)

class DoorR(Tile):

    def __init__(self, coords):
        self.image = load_image("door-r.png")
        self.nature = "floor"
        Tile.__init__(self, coords)

class DoorL(Tile):

    def __init__(self, coords):
        self.image = load_image("door-l.png")
        self.nature = "floor"
        Tile.__init__(self, coords)

class DoorU(Tile):

    def __init__(self, coords):
        self.image = load_image("door-u.png")
        self.nature = "floor"
        Tile.__init__(self, coords)

class DoorD(Tile):

    def __init__(self, coords):
        self.image = load_image("door-d.png")
        self.nature = "floor"
        Tile.__init__(self, coords)

class Floor(Tile):

    def __init__(self, coords):
        self.image = load_image("floor.png")
        self.nature = "floor"
        Tile.__init__(self, coords)

class Passage(Tile):

    def __init__(self, coords):
        self.image = load_image("passage.png")
        self.nature = "floor"
        Tile.__init__(self, coords)
