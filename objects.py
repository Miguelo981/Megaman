# Sprite classes for platform game
import glob
import os

import pygame as pg
from Settings import *
vec = pg.math.Vector2


def load_images(folder_path):
    images = []
    os.chdir(folder_path)
    for files in sorted(glob.glob('*.png'), key=os.path.getmtime):
        images.append(folder_path + '/' + files)
    return images


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        #self.image = pg.Surface((30, 40))
        self.image = pg.Surface((14, 34))
        self.spawn_sprites = load_images(self.path + '\images\MM_spawn')
        self.spawn()
        self.image = pg.image.load(os.getcwd()+'\images\MM_WS.png') #images/MM_WS.png
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.right = True
        self.moving = False
        self.dashing = False
        self.timer = 0
        #self.last = pygame.time.get_ticks()
        self.clock = self.game.clock
        self.cooldown = 100
        self.animation_cooldown = 15
        self.animation_counter = 0
        self.counter = 0
        self.count = 0
        self.time = clock.tick()
        self.collide = False
        self.path = os.getcwd()
        self.move_right_sprites = load_images(self.path+'\images\MM_move_r')
        self.move_left_sprites = load_images(self.path+'\images\MM_move_l')

    def spawn(self):
        pass #TODO SPAWN ANIMATION

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -15

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time
        #print(self.counter)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if self.vel.x >= 0 and self.vel.x < 1.5 or self.vel.x > -1.5 and self.vel.x <= 0:
            self.moving = False
            self.count = 0

        if self.count == 8:
            self.count = 0

        if self.moving:
            if self.right:
                self.image = pg.image.load(self.move_right_sprites[self.count])
            else:
                self.image = pg.image.load(self.move_left_sprites[self.count])
            if self.animation_counter > self.animation_cooldown:
                self.count += 1
                self.animation_counter = 0
        else:
            if self.right:
                self.image = pg.image.load(self.path+'\images\MM_WS.png')
            else:
                self.image = pg.image.load(self.path + '\images\MM_WS_l.png')

        if keys[pg.K_LEFT] and not self.collide:
            self.acc.x = -PLAYER_ACC
            self.right = False
            self.moving = True
        if keys[pg.K_RIGHT] and not self.collide:
            self.acc.x = PLAYER_ACC
            self.right = True
            self.moving = True
        #TODO CONTROL DEL DASH
        if keys[pg.K_a] and keys[pg.K_LEFT]:
            if self.counter > self.cooldown:
                self.moving = True
                for i in range(1,5):
                    self.vel.x -= 0.75
                    hits = pg.sprite.spritecollide(self, self.game.platforms, False)
                    if hits:
                        self.vel.x -= 0.75
                    #self.acc.x = -PLAYER_ACC
                    #self.pos.x -= 1
                self.counter = 0
                #self.vel.x = 0

        if keys[pg.K_a] and keys[pg.K_RIGHT]:
            self.moving = True
            if self.counter > self.cooldown:
                for i in range(1, 5):
                    self.vel.x += 1.5
                    #hits = pg.sprite.spritecollide(self, self.game.platforms, False)
                    #if hits:
                        #self.vel.x += 0.75
                self.counter = 0

        if not self.collide:
            # apply friction
            self.acc.x += self.vel.x * PLAYER_FRICTION
            # equations of motion
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, main):
        pg.sprite.Sprite.__init__(self)
        self.h = h
        self.w = w
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.main = main
