import os, sys
import pygame

from pygame.locals import *

def load_image(name, colorkey=None):
    path = os.path.join('images')
    path = os.path.join(path, name)
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print 'Cannot load image:', path
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

# grabs the sprite from the position in the spritesheet
# takes sheet,x,y,width,height
# coords are in units of 1 tile
#def grab_sprite(surface, x, y, w, h):
#    image = surface.subsurface(pygame.Rect(x*(data.tile_size+1), y*(data.tile_size+1), w*(data.tile_size+1), h*(data.tile_size+1)))
#    return image

def flash_red(image): # works, but is -extremely- slow
    for row in range(image.get_width()):
        for col in range(image.get_height()):
            if image.get_at((row, col)) != image.get_colorkey():
                image.set_at((row, col),
                             tint_pixel_red(image.get_at((row, col))[:3]))
    return image

def tint_pixel_red(color):
    r,g,b = color
    return (255,g,b,255)

#def fadeToBlack(rate):

#    mask = pygame.Surface((data.screen_width,data.screen_height))
#    counter = 0
#    while counter < 256:
#	data.display.drawAll()
#	mask.fill((0,0,0))
#	mask.set_alpha(counter)
#	data.screen.blit(mask,(0,0))
#	counter += rate
#	pygame.time.wait(data.ms_per_refresh)

#def fadeFromBlack(rate):

#    mask = pygame.Surface((data.screen_width,data.screen_height))
#    counter = 255
#    while counter > -1:
#	data.display.drawAll()
#	mask.fill((0,0,0))
#	mask.set_alpha(counter)
#	data.screen.blit(mask,(0,0))
#	counter -= rate
#	pygame.time.wait(data.ms_per_refresh)
