# Sprite classes for platform game
import glob, os

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
        self.life = Life_Bar(100, "Boss", 5, 75, GREEN)
        self.game = game
        #self.image = pg.Surface((30, 40))
        self.img = pg.image.load(path+'\images\MM_WS.png')
        #self.image = pg.Surface((15, 34)) #14, 34 informarme sobre el pg.surface
        #self.image = pg.image.load(os.getcwd()+'\images\MM_WS.png') #images/MM_WS.png
        #self.image.fill(YELLOW)
        self.rect = pygame.Rect(100,100,15,34)
        self.rect.x = 50
        self.rect.y = 50
        #self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH / 2, HEIGHT / 2)
        #self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.pos = pygame.Rect(100,100,15,34)
        self.pos.x = 50
        self.pos.y = 50
        #self.pos = vec(50,50)
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
        self.spawn_sprites = load_images(path + '\images\MM_spawn')
        self.move_right_sprites = load_images(path+'\images\MM_move_r')
        self.move_left_sprites = load_images(path+'\images\MM_move_l')
        self.shoot_sprite = load_images(path+'\images\MM_shoot')
        self.shoot_running_sprite = load_images(path + '\images\MM_shoot_moving')
        self.shoot = False
        self.shoots = []

    def spawn(self):
            if self.animation_counter > self.animation_cooldown and self.count <= 11:
                self.image = pg.image.load(self.spawn_sprites[self.count])
                self.count += 1

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        self.rect.y -= 5
        if hits:
            self.vel.y = -15
        else:
            self.rect.y += 2

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time
        #print(self.counter)

    def update(self):
        if self.life.life <= 0:
            print("muerto")
        #self.image.blit(pg.image.load(self.path+'\images\MM_WS.png'),(200, 300))
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if self.vel.x >= 0 and self.vel.x < 1 or self.vel.x > -1 and self.vel.x <= 0:
            self.moving = False
            self.count = 0

        if self.count == 4 and self.shoot and not self.moving:
            self.count = 0

        if self.count == 8 and self.moving:
            self.count = 0

        if self.shoot:
            if not self.moving:
                self.img = pg.image.load(self.shoot_sprite[self.count])
            elif self.moving:
                self.img = pg.image.load(self.shoot_running_sprite[self.count])

        if self.moving:
            if not self.shoot:
                self.image = pg.image.load(self.move_right_sprites[self.count])
                self.img = pg.image.load(self.move_right_sprites[self.count])
                #self.rect = pygame.Rect(self.rect.x, self.rect.y, 28, 33)
            '''elif not self.shoot:
                self.image = pg.image.load(self.move_left_sprites[self.count])
                self.img = pg.image.load(self.move_left_sprites[self.count])
                #self.rect = pygame.Rect(self.rect.x, self.rect.y, 28, 33)'''
        else:
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 15, 34) #x+13
            #print(self.rect.x)
            if not self.shoot:
                self.image = pg.image.load(path+'\images\MM_WS.png')
                self.img = pg.image.load(path + '\images\MM_WS.png')
            elif not self.shoot:
                self.image = pg.image.load(path + '\images\MM_WS_l.png')
                self.img = pg.image.load(path + '\images\MM_WS_l.png')
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
            self.image = pg.image.load(path + '\images\MM_WS_dash_1.png')
            self.img = pg.image.load(path + '\images\MM_WS_dash_1.png')
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
            #self.pos += self.vel + 0.5 * self.acc
            # wrap around the sides of the screen
        if self.rect.x > WIDTH:
            self.rect.x = WIDTH
        if self.rect.x < 0:
            self.rect.x = 0

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        #self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, main, color):
        pg.sprite.Sprite.__init__(self)
        self.h = h
        self.w = w
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.main = main

class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((30, 40))
        #self.img = pg.image.load(self.path + '\images\MM_WS.png')
        self.rect = pygame.Rect(0, 0, 8, 8)
        self.right = player.right
        if self.right:
            self.rect.x = player.rect.x+24
        else:
            self.rect.x = player.rect.x-24
        self.rect.y = player.rect.y+4
        self.init_rect = self.rect.x
        #self.img = pg.image.load(r'Megaman\images\blocks\grass.png')
        self.right = player.right
        self.active = True
        self.count = 0
        self.shoot_sprites = load_images(path + '\images\MM_shoot_1')
        #self.spawn_sprites = load_images(self.path + '\images\shoot')

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time

    def update(self):
        self.img = pg.image.load(self.shoot_sprites[self.count])

        '''if self.animation_counter > self.animation_cooldown:
            self.count += 1
            self.animation_counter = 0'''

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

class Enemy(pg.sprite.Sprite):
    def __init__(self, life, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.life = Life_Bar(life)
        # self.image = pg.Surface((30, 40))
        #TODO SPRITE self.img = pg.image.load(path + '\images\MM_WS.png')
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.right = True
        self.moving = False
        self.timer = 0
        self.cooldown = 100
        self.animation_cooldown = 15
        self.animation_counter = 0
        self.counter = 0
        self.count = 0
        self.time = clock.tick()
        self.shoot = False
        self.shoots = []

    def update(self):
        pass

    def behavior(self):
        pass

class Boss(Enemy):
    def __init__(self, enemy):
        self.enemy = enemy

#TODO QUE LAS BARRAS DE LOS NO-BOSSES SIGA AL ENEMIGO EN LA CABEZA
class Life_Bar(pg.sprite.Sprite):
    def __init__(self, max_life, type, w, h, color):
        pg.sprite.Sprite.__init__(self)
        self.max_life = max_life
        self.life = self.max_life
        self.vissible = False
        self.lifebar = Platform(0, 0, w, h, False, color)
        self.type = type

    def update(self):
        pass

    def quit_life(self, life):
        self.life -= life

    def add_life(self, life):
        self.life += life
        if self.life > self.max_life:
            self.life = self.max_life