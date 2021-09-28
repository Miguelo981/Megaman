import glob, random
from game import Settings

import pygame as pg
from game.Settings import *
vec = pg.math.Vector2

def load_images(folder_path):
    images = []
    os.chdir(folder_path)
    for files in sorted(glob.glob('*.png'), key=os.path.getmtime):
        images.append(os.path.join(folder_path, files))
    return images

#Objeto bala
class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 8, 8)
        self.right = player.right
        if self.right:
            self.rect.x = player.rect.x+24#-Game.scroll[0]
        else:
            self.rect.x = player.rect.x#+Game.scroll[0]
        self.init_rect = self.rect.x
        self.right = player.right
        self.special = False
        self.active = True
        self.count = 0
        if not self.special:
            self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/"+name+"/MM_bullet/1.png"))
            self.rect.y = player.rect.y + 8
        else:
            self.rect.y = player.rect.y + 4
        self.shoot_sprites = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_shoot_1"))

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time

    def update(self):
        if self.special:
            self.img = pg.image.load(self.shoot_sprites[self.count])

        if self.rect.x < (self.init_rect+120) and self.right:
            self.rect.x += 10
            self.count += 1
        elif self.rect.x > (self.init_rect-120) and not self.right:
            self.rect.x -= 10
            self.count += 1
        else:
            self.active = False
        if self.count > 4:
            self.count = 0

#Objeto carga del buster
class Charge(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.charge1_sprites = load_images(os.path.join(ASSETS_PATH, "images/"+name+"/MM_charge1"))
        self.player = player
        self.clock = self.player.clock
        self.counter = 0
        self.animation_counter = 0
        self.img = pg.image.load(self.charge1_sprites[0])
        self.rect = pygame.Rect(100, 100, 15, 34)
        self.rect.x = self.player.rect.x / 2
        self.rect.y = self.player.rect.y / 2
        self.animation_cooldown = 10

    def set_clock(self):
        if self.animation_counter > 100:
            self.counter += 1
        else:
            self.animation_counter += self.player.time

    def update(self, *args):
        if self.player.right:
            self.rect.x = self.player.rect.x+26
            self.rect.y = self.player.rect.y +4
        else:
            self.rect.x = self.player.rect.x - 8
            self.rect.y = self.player.rect.y +4

        if self.player.charging and self.counter < len(self.charge1_sprites):
            self.img = pg.image.load(self.charge1_sprites[self.counter])
            self.time = 0
        elif self.counter == len(self.charge1_sprites):
            self.counter = 0
            self.time = 0

        if self.animation_counter > self.animation_cooldown:
            self.counter += 1
            self.animation_counter = 0

class Bullet2(pg.sprite.Sprite):
    def __init__(self, minion):
        pg.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 8, 8)
        self.right = minion.right
        if self.right:
            self.rect.x = minion.rect.x+24
        else:
            self.rect.x = minion.rect.x-24
        self.init_rect = self.rect.x
        self.right = minion.right
        self.active = True
        self.count = 0
        self.rect.y = minion.rect.y + 4
        self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/Enemies/minion/bullet/0.png"))
        self.bullet_sprites = load_images(os.path.join(ASSETS_PATH, "images/Enemies/minion/bullet"))

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time

    def update(self):
        self.img = pg.image.load(self.bullet_sprites[self.count])

        if self.rect.x < (self.init_rect+120) and self.right:
            self.rect.x += 5
            self.count += 1
        elif self.rect.x > (self.init_rect-120) and not self.right:
            self.rect.x -= 5
            self.count += 1
        else:
            self.active = False
        if self.count > 4:
            self.count = 0

#Objeto del drop de enemigos
class Drop(pg.sprite.Sprite):
    def __init__(self, enemy):
        pg.sprite.Sprite.__init__(self)
        self.enemy = enemy
        self.type = ""
        self.vel = vec(0, 0)
        self.vertical_momentum = 0
        self.sprites = []
        self.createType()
        self.count = 0
        if self.type != "None":
            self.rect.x = self.enemy.rect.x
            self.rect.y = self.enemy.rect.y

    def createType(self):
        num = random.randint(1, 10)
        if num > 9:
            self.type = "life"
            self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/objects/life.png"))
            self.rect = pygame.Rect(0, 0, 16, 15)
        elif num > 7:
            self.type = "heal"
            self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/objects/heal/4.png"))
            self.sprites = load_images(os.path.join(ASSETS_PATH, "images/objects/heal"))
            self.rect = pygame.Rect(0, 0, 16, 8)
        elif num > 4:
            self.type = "points"
            self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/objects/points/1.png"))
            self.sprites = load_images(os.path.join(ASSETS_PATH, "images/objects/points"))
            self.rect = pygame.Rect(0, 0, 13, 16)
        else:
            self.type = "None"
            self.kill()

    def effect(self):
        if self.type == "life":
            Settings.lifes += 1
        if self.type == "heal":
            self.enemy.game.player.life.add_life(5)
        if self.type == "points":
            Settings.points += 50
        self.type = "None"
        self.kill()

    def update(self):
        if self.count < len(self.sprites) and len(self.sprites) > 0:
            self.img = pg.image.load(self.sprites[self.count])
            self.count += 1
        else:
            self.count = 0

#Objeto de las barras de vida de los enemigos, jugador y Omega
class Life_Bar(pg.sprite.Sprite):
    def __init__(self, type, w, h, color):
        pg.sprite.Sprite.__init__(self)
        self.max_life = h
        self.vissible = False
        self.color = color
        self.w = w
        self.h = h
        self.background = pg.Surface((self.w, self.h))
        self.background.fill(DARK)
        self.image = pg.Surface((self.w, self.h)).convert()
        self.image.fill(self.color)
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.x = 5
        self.rect.y = 38
        self.type = type
        self.constant_dmg = 0
        self.counter = 0

    def set_clock_player(self, time):
        if self.constant_dmg == 1:
            self.counter += time

    def set_clock(self, clock):
        if self.constant_dmg == 3:
            self.time = clock.tick()
            self.counter += self.time

    def update(self):
        pass

    def inmunity_player(self):
        if self.constant_dmg == 1:
            if self.counter > 1500:
                self.constant_dmg = 0
                self.counter = 0
                return False
            else:
                return True
        else:
            return False

    def inmunity(self):
        if self.constant_dmg == 3:
            if self.counter > 50:
                self.constant_dmg = 0
                self.counter = 0
                return False
            else:
                return True
        else:
            return False

    def quit_life(self, life):
        if not self.inmunity_player():
            self.h -= life
            self.constant_dmg +=1
            if self.h < 0:
                self.h = 0
            self.image = pg.Surface((self.w, self.h))
            self.image.fill(self.color)

    def quit_enemy_life(self, life):
        if not self.inmunity():
            self.constant_dmg += 1
            self.w -= life
            if self.w < 0:
                self.w = 0
            self.image = pg.Surface((self.w, self.h))
            self.image.fill(self.color)

    def quit_minion_life(self, life):
        self.w -= life
        if self.w < 0:
            self.w = 0
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)

    def add_life(self, life):
        self.h += life
        if self.h > self.max_life:
            self.h = self.max_life
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)

#Objeto de la puerta
class Door(pg.sprite.Sprite):
    def __init__(self, x, y, scene):
        pg.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 43, 88)
        self.rect.x = x
        self.rect.y = y
        self.count = 0
        self.scene = scene
        self.sprites = load_images(os.path.join(ASSETS_PATH, "images/blocks/door"))
        self.img = pg.image.load(os.path.join(ASSETS_PATH, "images/blocks/door/0.png"))
        self.box = InivisbleWall(x+10,y,22,88)

    def update(self):
        if self.count > 15:
            self.box = None
        else:
            self.box = InivisbleWall(self.rect.x + 10, self.rect.y, 22, 88)

    def open(self):
        self.img = pg.image.load(self.sprites[self.count])
        if self.count < len(self.sprites)-1:
            self.count += 1
        else:
            self.img = pg.image.load(self.sprites[16])

    def close(self):
        if self.count >= 0:
            self.img = pg.image.load(self.sprites[self.count])
            self.count -= 1

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, main, color):
        pg.sprite.Sprite.__init__(self)
        self.h = h
        self.w = w
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.rect.x = x
        self.rect.y = y
        self.main = main

class InivisbleWall(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.h = h
        self.w = w
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(WHITE)
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.rect.x = x
        self.rect.y = y