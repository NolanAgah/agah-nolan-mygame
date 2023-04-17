# File created by NOLAN AGAH
# Sources:
    # https://www.youtube.com/watch?v=wfcWRAxRVBA
    # https://www.youtube.com/watch?v=JLUqOmE9veI
    # https://www.youtube.com/watch?v=0TicWQno99U

'''
My goal is:

Create coin collection system with sounds, images and counter

'''

# import libs
import pygame as pg
import os
# import settings 
from settings import *
from sprites import *
from os import path
import sys
import time

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "sounds")

def draw_text(screen, text, size, x, y, color):
    font = pg.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
        print(self.screen)

    # set up sounds
    def load_data(self):
        self.coin_img = pg.image.load(path.join(img_folder, "coin.png")).convert()
        self.coin_sound = pg.mixer.Sound(path.join(snd_folder, "coin_collect.mp3"))

    def new(self):
        # starting a new game
        self.load_data()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.coin1 = Coin(self, 350, 200)
        self.player = Player(self)
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        self.all_sprites.add(self.plat1)
        self.all_sprites.add(self.coin1)

        self.platforms.add(self.plat1)
        self.coins.add(self.coin1)

        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            if len(plat) == 6:
                p = Platform(*plat)
            # add the moving platform
            elif len(plat) == 7:
                p = MovingPlatform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        # add all mobs
        for i in range(0,10):
            m = Mob(20,20,(0,255,0))
            self.all_sprites.add(m)
            self.enemies.add(m)
        self.run()
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            # stops music if player is not invincible
            if event.type == pg.USEREVENT:
                self.player.invincible = False
                pg.mixer.music.stop()
    # draws health bar
    def draw_health(self):
        # draws the health bar as a percentage of players health--see sources
        health_percentage = self.player.health / PLAYER_MAX_HEALTH
        health_width = int(health_percentage * 200)
        health_bar = pg.Rect(20, 20, health_width, 20)
        pg.draw.rect(self.screen, RED, health_bar)
        pg.draw.rect(self.screen, WHITE, (20, 20, 200, 20), 2)
    def update(self):
        self.all_sprites.update()
        check_coin_collision(self)
        # if the player hits a score of ten, they will gain the invicible powerup
        if self.score == 10:
            self.player.invincible = True
            self.player.invincible_time = 5 * FPS
            self.player.image.fill(RED)
            PLAYER_ACC = 4
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if hits[0].variant == "disappearing":
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
        # if players health hits zero
        if self.player.health <= 0:
            # render "Game Over" text aon the screen
            draw_text(self.screen, "Game Over", 50, WIDTH / 2, HEIGHT / 2, RED)
            pg.display.flip()
            # pause the game for 2 seconds
            time.sleep(2)
            # close the window
            pg.quit()
            sys.exit()
        # Coin collection
        coin_hits = pg.sprite.spritecollide(self.player, self.coins, True)
        # adds to score and plays sound when player hits coin
        for coin in coin_hits:
            self.score += 1
            self.coin_sound.play()

    
    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        # draw the score
        self.draw_text(f"Score: {self.score}", 22, WHITE, WIDTH // 2, 10)
        self.draw_health()
        pg.display.flip()
    
    # sets up draw text method
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    

# instantiate the game class
g = Game()

# start game loop
while g.running:
    g.new()

pg.quit()
