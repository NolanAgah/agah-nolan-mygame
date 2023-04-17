# file created by NOLAN AGAH
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
import os
import random

vec = pg.math.Vector2

# game_folder = os.path.dirname(__file__)

# player class

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties
        self.game = game
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.health = PLAYER_MAX_HEALTH
        self.invincible = False
        self.invincible_time = 0
    def input(self):
        keystate = pg.key.get_pressed()
        # if keystate[pg.K_w]:
        #     self.acc.y = -PLAYER_ACC
        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        # if keystate[pg.K_s]:
        #     self.acc.y = PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
        # if keystate[pg.K_p]:
        #     if PAUSED == False:
        #         PAUSED = True
        #         print(PAUSED)
        #     else:
        #         PAUSED = False
        #         print(PAUSED)
    # ...
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def become_invincible(self):
        self.invincible = True
        sound_folder = os.path.join(os.path.dirname(__file__), "sounds")
        coin_pickup_sound = os.path.join(sound_folder, 'powerup.mp3')
        pg.mixer.Sound(coin_pickup_sound).play()
        # set a timer for 5 seconds (5000 milliseconds)
        pg.time.set_timer(pg.USEREVENT, 5000)

    
    
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("i am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("i am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            print("i am off the bottom of the screen")
        if self.rect.y < 0:
            print("i am off the top of the screen...")
    
    # defines powerup
    def power_up(self):
        self.image.fill(RED)
        global PLAYER_ACC
        PLAYER_ACC = 2.5
    def mob_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            # if the player is not invincible, then they will lose 10 health everytime they collide with mob
            if not self.invincible:
                print("you collided with an enemy...")
                self.game.player.health -= 10
                if self.game.player.health < 0:
                    self.game.player.health = 0


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.mob_collide()
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.invincible_time > 0:
            self.invincible_time -= 1
            if self.invincible_time == 0:
                self.invincible = False
                self.image.fill(BLACK)
                PLAYER_ACC = 2
class Coin(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self)
        self.game = game
        self.image = game.coin_img
        # self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Mob(Sprite):
    def __init__(self,width,height, color):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.pos = vec(self.rect.center)
        self.vel = vec(randint(1,5),randint(1,5))
        self.acc = vec(1,1)
        self.cofric = 0.01
    # ...
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.x < 0:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y < 0:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
    def update(self):
        self.inbounds()
        # self.pos.x += self.vel.x
        # self.pos.y += self.vel.y
        self.pos += self.vel
        self.rect.center = self.pos

# create a new platform class...


class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant

# I had to create a new class for the moving platform
class MovingPlatform(Platform):
    # adds parameters to fit inside the plat_list
    def __init__(self, x, y, width, height, color, variant, move_speed):
        super().__init__(x, y, width, height, color, variant)
        self.move_speed = move_speed

    def update(self):
        # bounces off top and bottom of screen
        self.rect.y += self.move_speed
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.move_speed = -self.move_speed

# everything that happens when the player hits the coin
def check_coin_collision(game):
    hits = pg.sprite.spritecollide(game.player, game.coins, True)
    if hits:
        game.score += 1
        # add coin collection sound effect
        sound_folder = os.path.join(os.path.dirname(__file__), "sounds")
        coin_pickup_sound = os.path.join(sound_folder, 'coin_collect.mp3')
        pg.mixer.Sound(coin_pickup_sound).play()
        # got this from source--dont rly know why it's needed
        if game.score % 10 == 0:
            game.player.become_invincible()
        # spawn a new coin at a random location
        x = randint(50, WIDTH - 50)
        y = randint(50, HEIGHT - 100)
        new_coin = Coin(game, x, y)
        game.all_sprites.add(new_coin)
        game.coins.add(new_coin)