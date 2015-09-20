import pygame

class Creature(pygame.sprite.Sprite):

    def __init__(self, (x,y)):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = 18*x # HARDCODED GLOBALS
        self.rect.y = 18*y
        self.x = x
        self.y = y

    def move(self, x, y):
        # use for normal movement, teleporting, etc, etc...
        self.rect.x = 18*x # HARDCODED GLOBALS
        self.rect.y = 18*y
        self.x = x
        self.y = y
