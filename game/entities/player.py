import random

import pygame as pg

from game import Settings
from game.Settings import *

from conf import ASSETS_PATH
from game.entities.objects import Life_Bar, load_images, Charge

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.life = Life_Bar("Boss", 6, 42, GREEN)
        self.game = game
        self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/MM_WS.png'))
        self.rect = pygame.Rect(100,100,15,34)
        self.rect.x = 50
        self.rect.y = 50
        self.vel = vec(0, 0)
        self.right = True
        self.moving = False
        self.dashing = False
        self.timer = 0
        self.clock = self.game.clock
        self.cooldown = 100
        self.animation_cooldown = 15
        self.animation_counter = 0
        self.counter = 0
        self.count = 0
        self.time = clock.tick()
        self.collide = False
        self.move_right_sprites = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_move_r"))
        self.move_left_sprites = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_move_l"))
        self.shoot_sprite = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_shoot"))
        self.shoot_jump = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_jump_shoot"))
        self.shoot_running_sprite = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_shoot_moving"))
        self.death_sprites = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_death"))
        self.dmg_sprites = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_dmg"))
        self.charge = Charge(self)
        self.animation_death_counter = 0
        self.shoot = False
        self.shoots = []
        self.animation_dmg_counter = 0
        self.charging = False
        self.alive = True
        self.air = False
        self.sound = pygame.mixer.Sound

    def spawn(self):
            if self.animation_counter > self.animation_cooldown and self.count <= 11:
                self.image = pg.image.load(self.spawn_sprites[self.count])
                self.count += 1

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time

    def update(self):
        self.life.set_clock_player(self.time)
        if self.charging:
            self.charge.set_clock()
        self.charge.update()
        if self.life.constant_dmg == 1:
            self.dmg()
        else:
            self.animation_dmg_counter = 0
        if self.life.h <= 0:
            self.death()
        else:
            self.acc = vec(0, PLAYER_GRAV)
            keys = pg.key.get_pressed()
            if self.vel.x >= 0 and self.vel.x < 1 or self.vel.x > -1 and self.vel.x <= 0:
                self.moving = False
                self.count = 0

            if self.count == 4 and self.shoot and not self.moving or self.air:
                self.count = 0

            if self.count == 8 and self.moving:
                self.count = 0

            if self.life.inmunity_player() and random.randint(1, 4) == 1:
                self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/"+name+"/MM_WS_invisible.png"))
            else:
                if self.shoot:
                    if not self.moving and not self.air:
                        self.img = pg.image.load(self.shoot_sprite[self.count])
                    elif self.air:
                        self.img = pg.image.load(self.shoot_jump[self.count])
                    elif self.moving:
                        self.img = pg.image.load(self.shoot_running_sprite[self.count])

                if self.moving:
                    if not self.shoot:
                        self.image = pg.image.load(self.move_right_sprites[self.count])
                        self.img = pg.image.load(self.move_right_sprites[self.count])
                else:
                    self.rect = pygame.Rect(self.rect.x, self.rect.y, 15, 34)
                    if not self.shoot:
                        self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/"+name+"/MM_WS.png"))
                    elif not self.shoot:
                        self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/"+name+"/MM_WS_l.png"))
                    elif self.shoot_sprite:
                        self.img = pg.image.load(self.shoot_sprite[self.count])

            if self.animation_counter > self.animation_cooldown:
                self.count += 1
                self.animation_counter = 0

            if keys[pg.K_LEFT] and not self.collide:
                self.acc.x = -PLAYER_ACC
                self.rect.x -= 3
                self.right = False
                self.moving = True
            if keys[pg.K_RIGHT] and not self.collide:
                self.acc.x = PLAYER_ACC
                self.rect.x += 3
                self.right = True
                self.moving = True
            if keys[pg.K_a] and keys[pg.K_LEFT]:
                self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/"+name+"/MM_WS_dash_1.png"))
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 41, 18)
                self.right = False
                if self.counter > self.cooldown:
                    self.moving = True
                    for i in range(1,5):
                        self.rect.x -= 1
                    self.counter = 0

            if keys[pg.K_a] and keys[pg.K_RIGHT]:
                self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/"+name+"/MM_WS_dash_1.png"))
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 41, 18)
                self.moving = True
                if self.counter > self.cooldown:
                    for i in range(1, 5):
                        self.rect.x += 1
                    self.counter = 0

            if not self.collide:
                self.acc.x += self.vel.x * PLAYER_FRICTION
                self.vel += self.acc
            if self.rect.x < 0:
                self.rect.x = 0

    def dmg(self):
        if self.animation_dmg_counter < len(self.dmg_sprites):
            self.img = pg.image.load(self.dmg_sprites[self.animation_dmg_counter])
            self.animation_dmg_counter+=1

    def death(self):
        if self.life.h <= 0:
            self.able_to_move = False
            if self.animation_death_counter == 0:
                self.img = pg.image.load(self.shoot_sprite[self.animation_death_counter])
            if self.counter > 100 and self.animation_death_counter < len(self.death_sprites): #TODO ESCOGER OTRO COUNTER
                self.img = pg.image.load(self.death_sprites[self.animation_death_counter])
                self.animation_death_counter+=1
            elif self.alive:
                if Settings.lifes > 0:
                    Settings.lifes -= 1
                    pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(ASSETS_PATH, 'images/MMX09.wav')))
                else:
                    self.game.playing = False
                self.alive = False
