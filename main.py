# file created by NOLAN AGAH

# import libs
import pygame as pg

import random

import os

from os import path

from random import randint

# import settings

from settings import *

from sprites import *

# from pg.sprite import Sprite

class Game:
    def __init__(self):
        pg.init
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My game...")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for i in range(1,10):
            e = Mob()
            self.all_sprites.add(e)
        self.run()
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events():
        pass
    def update():
        pass
    def draw():
        pass
# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
def get_mouse_now():
    x,y = pg.mouse.get_pos()
    return (x,y)


# init pg and create window
pg.init()
# init sound mixer
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My first game...")
clock = pg.time.Clock()

player_img = pg.image.load(path.join(img_folder, "bell-ar-man.png")).convert()


# game loop

RUNNING = True

while RUNNING:
    #  keep loop running at the right speed
    ### process input events section of game loop
    for event in pg.event.get():
        # check for window closing
        if event.type == pg.QUIT:
            RUNNING = False
            # break
    # print(get_mouse_now())
    ### update section of game loop (if updates take longer the 1/30th of a second, you will get laaaaag...)
    all_sprites.update()

    blocks_hit_list = pg.sprite.spritecollide(player, enemies, False)
    for block in blocks_hit_list:
        # print(enemies)
        pass
    ### draw and render section of game loop
    screen.fill(BLUE)
    all_sprites.draw(screen)
    screen.blit(player_img, player.rect)
    # double buffering draws frames for entire screen
    pg.display.flip()
    # pg.display.update() -> only updates a portion of the screen
# ends program when loops evaluates to false
pg.quit()