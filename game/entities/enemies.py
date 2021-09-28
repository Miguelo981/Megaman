import random
from time import sleep

import pygame as pg

from game import Settings
from game.Settings import *

from conf import ASSETS_PATH

#Objeto minion, enemigo normal
from game.entities.objects import Life_Bar, load_images, Drop, Bullet


class Minion(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Enemies/minion/0.png'))
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.life = Life_Bar("Boss", 16, 4, RED)
        self.right = False
        self.moving = False
        self.timer = 0
        self.cooldown = 100
        self.animation_cooldown = 15
        self.animation_counter = 0
        self.counter = 0
        self.time = 0
        self.shoot = False
        self.shoots = []
        self.down = False
        self.clock = self.game.clock
        self.dmg_coldown = 100
        self.alive = True
        self.move_sprites = load_images(os.path.join(ASSETS_PATH, "images/Enemies/minion/movement"))

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        if self.shoot and self.counter > 125:
            self.shoot = False
            self.counter = 0

    def update(self):
        if (self.rect.x-250 <= self.game.player.rect.x <= self.rect.x) or (self.rect.x+250 >= self.game.player.rect.x >= self.rect.x):
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.img.get_rect()[2], self.img.get_rect()[3])
            self.life.set_clock(self.clock)
            if self.life.w <= 0:
                self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Enemies/minion/death/0.png'))
                if self.rect.y < 135:
                    self.rect.y +=random.randint(2,4);
                if self.alive:
                    self.alive = False
                    Settings.points += 20
                    if random.randint(1,3) != 3:
                        self.game.objects.append(Drop(self))
            else:
                self.alive = True
            if self.alive:
                self.behavior()

    def behavior(self):
        if self.rect.x-125 <= self.game.player.rect.x <= self.rect.x:
            self.right = False
            self.shoot_()
        elif self.rect.x+125 >= self.game.player.rect.x >= self.rect.x:
            self.right = True
            self.shoot_()
        else:
            if random.randint(1,25) == 1 or self.moving:
                self.moving = True
                if self.counter > 0:
                    if self.animation_counter < len(self.move_sprites):
                        self.img = pg.image.load(self.move_sprites[self.animation_counter])
                        self.animation_counter += 1
                    else:
                        self.animation_counter = 0
                    self.counter = 0.5
                if self.right and self.rect.x <= (self.x+50):
                    self.rect.x += 2
                elif not self.right and self.rect.x >= (self.x-50):
                    self.rect.x -= 2
                else:
                    self.moving = False
                    self.right = not self.right
                    self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Enemies/minion/0.png'))
            if self.rect.y >= 110 and not self.shoot_():
                self.rect.y -= 4

    def shoot_(self):
        if not self.shoot:
            self.shoots.append(Bullet(self))
            self.shoot = True
        if self.rect.y <= 110:
            self.rect.y += 4
        self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Enemies/minion/shoot/0.png'))
