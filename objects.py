import glob, os, random, pygame, Settings, Game

import pygame as pg
from Settings import *
vec = pg.math.Vector2

#TODO SI MUERES ANTES QUE EL BOSS, CANCELAR BULLETS / ENEMY INVENCIBILITY

def load_images(folder_path):
    images = []
    os.chdir(folder_path)
    for files in sorted(glob.glob('*.png'), key=os.path.getmtime):
        images.append(folder_path + '/' + files)
    return images

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.life = Life_Bar("Boss", 6, 42, GREEN)
        self.game = game
        self.img = pg.image.load(path+'\images\MM_WS.png')
        self.rect = pygame.Rect(100,100,15,34)
        self.rect.x = 50
        self.rect.y = 50
        self.vel = vec(0, 0)
        #self.acc = vec(0, 0)
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
        #self.spawn_sprites = load_images(path + r"\images\""+name+"\MM_spawn")
        self.move_right_sprites = load_images(path+r"\images"+name+"\MM_move_r")
        self.move_left_sprites = load_images(path+r"\images"+name+"\MM_move_l")
        self.shoot_sprite = load_images(path+r"\images"+name+"\MM_shoot")
        self.shoot_jump = load_images(path + r"\images"+name+"\MM_jump_shoot")
        self.shoot_running_sprite = load_images(path + r"\images"+name+"\MM_shoot_moving")
        self.death_sprites = load_images(path + r"\images"+name+"\MM_death")
        self.dmg_sprites = load_images(path + r"\images"+name+"\MM_dmg")
        self.charge = Charge(self)
        self.animation_death_counter = 0
        self.shoot = False
        self.shoots = []
        self.animation_dmg_counter = 0
        self.charging = False
        self.alive = True
        self.air = False

    def spawn(self):
            if self.animation_counter > self.animation_cooldown and self.count <= 11:
                self.image = pg.image.load(self.spawn_sprites[self.count])
                self.count += 1

    def set_clock(self):
        self.time = self.clock.tick()
        self.counter += self.time
        self.animation_counter += self.time
        #print(self.counter)

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
                self.img = pg.image.load(path + r"\images"+name+"\MM_WS_invisible.png")
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
                        #self.rect = pygame.Rect(self.rect.x, self.rect.y, 28, 33)
                    '''elif not self.shoot:
                        self.image = pg.image.load(self.move_left_sprites[self.count])
                    self.img = pg.image.load(self.move_left_sprites[self.count])
                    #self.rect = pygame.Rect(self.rect.x, self.rect.y, 28, 33)'''
                else:
                    self.rect = pygame.Rect(self.rect.x, self.rect.y, 15, 34) #x+13
                    #print(self.rect.x)
                    if not self.shoot:
                        self.img = pg.image.load(path + r"\images"+name+"\MM_WS.png")
                    elif not self.shoot:
                        self.img = pg.image.load(path + r"\images"+name+"\MM_WS_l.png")
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
                self.img = pg.image.load(path + r"\images"+name+"\MM_WS_dash_1.png")
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 41, 18)
                self.right = False
                if self.counter > self.cooldown:
                    self.moving = True
                    for i in range(1,5):
                        self.rect.x -= 1
                    self.counter = 0

            if keys[pg.K_a] and keys[pg.K_RIGHT]:
                #self.image = pg.image.load(path + '\images\MM_WS_dash_1.png')
                self.img = pg.image.load(path + r"\images"+name+"\MM_WS_dash_1.png")
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 41, 18)
                self.moving = True
                if self.counter > self.cooldown:
                    for i in range(1, 5):
                        self.rect.x += 1
                    self.counter = 0

            if not self.collide:
                self.acc.x += self.vel.x * PLAYER_FRICTION
                # equations of motion
                self.vel += self.acc
            #if self.rect.x > WIDTH:
             #   self.rect.x = WIDTH
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
            else:
                self.alive = False



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
            self.img = pg.image.load(path + r"\images"+name+r"\MM_bullet\1.png")
            self.rect.y = player.rect.y + 8
        else:
            self.rect.y = player.rect.y + 4
        self.shoot_sprites = load_images(path + r"\images"+name+"\MM_shoot_1")

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

class Charge(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.charge1_sprites = load_images(path + r"\images"+name+"\MM_charge1")
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

class Minion(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.img = pg.image.load(path + r'\images\Enemies\minion\0.png')
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.life = Life_Bar("Boss", 32, 4, RED)
        self.right = False
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
        self.down = False
        self.clock = self.game.clock
        self.dmg_coldown = 100
        self.assault = False
        self.alive = True

    def update(self):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.img.get_rect()[2], self.img.get_rect()[3])
        self.life.set_clock(self.clock)
        if self.life.w <= 0:
            self.alive = False
            self.img = pg.image.load(path + r'\images\Enemies\minion\death\0.png')
            if self.rect.y < 135:
                self.rect.y +=random.randint(2,4);
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
            if random.randint(1,5) == 1 or self.moving:
                self.moving = True
                if self.right and self.rect.x <= (self.x+50):
                    self.rect.x += 2
                elif not self.right and self.rect.x >= (self.x-50):
                    self.rect.x -= 2
                else:
                    self.moving = False
                    self.right = not self.right
                    if self.rect.y >= 110:
                        self.rect.y -= 5
                    self.img = pg.image.load(path + r'\images\Enemies\minion\0.png')

    def shoot_(self):
        if not self.shoot:
            self.shoots.append(Bullet(self))
            self.shoot = True
        self.img = pg.image.load(path + r'\images\Enemies\minion\shoot\0.png')
        if self.rect.y <= 110:
            self.rect.y += 5

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
        self.img = pg.image.load(path + r"\images\Enemies\minion\bullet\0.png")
        self.bullet_sprites = load_images(path + r"\images\Enemies\minion\bullet")

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

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.img = pg.image.load(path + '\images\Bosses\Omega\main.png')
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.life = Life_Bar("Boss", 84, 6, RED)
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
        self.down = False
        self.clock = self.game.clock
        self.dmg_coldown = 100
        self.assault = False

    def update(self):
        self.life.set_clock(self.clock)
        if self.life.constant_dmg == 3:
            if random.randint(1, 6) == 1:
                self.img = pg.image.load(path + '\images\Bosses\Omega\main.png')
            else:
                self.img = pg.image.load(path + '\images\Bosses\Omega\damage.png')
            self.life.inmunity()
        else:
            self.img = pg.image.load(path + '\images\Bosses\Omega\main.png')

        if self.rect.y < (self.y+10) and not self.down and not self.assault:
            self.rect.y += 1
        else:
            self.down = True
        if self.rect.y > (self.y-10) and self.down and not self.assault:
            self.rect.y -= 1
        else:
            self.down = False

    def behavior(self):
        pass

class Omega(pg.sprite.Sprite):
    def __init__(self, enemy, player):
        pg.sprite.Sprite.__init__(self)
        self.enemy = enemy
        self.left_hand = Left_hand(self.enemy.rect.x, self.enemy.rect.y, player)
        self.right_hand = Right_hand(self.enemy.rect.x, self.enemy.rect.y, player)
        self.ball = None #TODO array of balls
        self.ball2 = None
        self.invisibleWall = InivisbleWall(self.enemy.rect.x+20, self.enemy.rect.y, 100, 143)

    def update(self):
        self.enemy.update()
        self.left_hand.update(self.enemy)
        self.right_hand.update(self.enemy)
        if self.ball != None:
            self.ball.update(True)
        if self.ball2 != None:
            self.ball2.update(True)
        if self.enemy.life.constant_dmg == 3: #self.right_hand.rings_number < 2 or self.left_hand.rings_number < 2
            self.enemy.assault = True
            self.left_hand.attack()
            if self.enemy.life.w < 60:
                self.right_hand.attack()
            if self.enemy.life.w < 70:
                self.ball = Ball(self, random.randint(1,6))
            if self.enemy.life.w < 30 and self.ball.rect.x < self.enemy.rect.x-30:
                self.ball2 = Ball(self, self.ball.incx)
        '''else:
            self.ball = None'''
        if self.left_hand.rings_number == 3:
            self.enemy.assault = False

class Left_hand(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        pg.sprite.Sprite.__init__(self)
        self.base = pg.image.load(path + '\images\Bosses\Omega\left_hand.png')
        self.open = pg.image.load(path + '\images\Bosses\Omega\hand_open.png')
        self.left = False
        self.img = self.base
        self.rect = pygame.Rect(self.img.get_rect())
        self.basex = x+6
        self.basey = y+60
        self.rect.x = self.basex
        self.rect.y = self.basey
        self.attacking = False
        self.player = player
        self.able_to_move = True
        self.attack_coldown = 350
        self.rings = load_images(path+r'\images\Bosses\Omega\V_Rings')
        self.counter = 0
        self.rings_number = 0
        self.ring = None
        self.left_mode = True

    def update(self, enemy):
        if not self.attacking:
            self.rect.x = enemy.rect.x+6
            self.rect.y = enemy.rect.y+60
        if self.attacking:
            self.left = True
            if self.rect.y > 0 and self.able_to_move:
                self.rect.y -=3
            elif self.rect.x > 25 and self.able_to_move and self.rect.x+1 != self.player.rect.x and self.rect.x-1 != self.player.rect.x and self.rect.x != self.player.rect.x and self.left_mode:
                self.rect.x -=3
            elif self.rect.x < self.basex-50 and self.able_to_move and self.rect.x + 1 != self.player.rect.x and self.rect.x - 1 != self.player.rect.x and self.rect.x != self.player.rect.x and not self.left_mode:
                self.rect.x +=3
            else:
                self.able_to_move = False
                if self.rings_number < 3:
                    self.shoot()
                else:
                    self.ring = None
                    self.attacking = False
                    self.rings_number = 0
                    self.left = False
                    self.able_to_move = True
                    self.img = self.base

    def shoot(self):
        if self.counter < len(self.rings):
            self.ring = Ring(self.rect.x, self.rect.y, pg.image.load(self.rings[self.counter]).get_rect())
            self.ring.img = pg.image.load(self.rings[self.counter])
            self.counter += 1
        if self.ring.rect.y < HEIGHT-350:
            self.ring.rect.y += 4
        else:
            self.ring.kill()
            self.rings_number += 1
            self.counter = 0
            self.able_to_move = True
            if self.rect.x < 25:
                self.left_mode = False
            else:
                self.left_mode = True

    def attack(self):
        self.attacking = True
        self.img = self.open
        #self.attacking = False

class Right_hand(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        pg.sprite.Sprite.__init__(self)
        self.base = pg.image.load(path + r'\images\Bosses\Omega\right_hand.png')
        self.open = pg.image.load(path + r'\images\Bosses\Omega\r_open.png')
        self.img = self.base
        self.rect = pygame.Rect(self.img.get_rect())
        self.basex = x-6
        self.basey = y+60
        self.rect.x = self.basex
        self.rect.y = self.basey
        self.attacking = False
        self.player = player
        self.able_to_move = True
        self.attack_coldown = 350
        self.rings = load_images(path+'\images\Bosses\Omega\Ring')
        self.counter = 0
        self.rings_number = 0
        self.ring = None
        self.down_mode = True

    def update(self, enemy):
        if not self.attacking:
            self.rect.x = enemy.rect.x+50
            self.rect.y = enemy.rect.y+65
        if self.attacking:
            self.left = True
            if self.rect.y < 110 and self.able_to_move and self.down_mode:
                self.rect.y +=3
            elif self.rect.y > 50 and self.able_to_move and self.rect.y+1 != self.player.rect.y and self.rect.y-1 != self.player.rect.y and self.rect.y != self.player.rect.y and not self.down_mode:
                self.rect.y -=3
            else:
                self.able_to_move = False
                if self.rings_number < 3:
                    self.shoot()
                else:
                    self.ring = None
                    self.attacking = False
                    self.rings_number = 0
                    self.able_to_move = True
                    self.img = self.base

    def shoot(self):
        if self.counter < len(self.rings):
            self.ring = Ring(self.rect.x, self.rect.y, pg.image.load(self.rings[self.counter]).get_rect())
            self.ring.img = pg.image.load(self.rings[self.counter])
            self.counter += 1
        if self.ring.rect.x > -25:
            self.ring.rect.x -= 4
        else:
            if self.rect.x > 75:
                self.rect.x -= 18
            self.ring.kill()
            self.rings_number += 1
            self.counter = 0
            self.able_to_move = True
            if self.rect.y < 110:
                self.down_mode = True
            else:
                self.down_mode = False

    def attack(self):
        self.attacking = True
        self.img = self.open
        #self.attacking = False

class Ring(pg.sprite.Sprite):
    def __init__(self, x, y, rect):
        pg.sprite.Sprite.__init__(self)
        self.img = None
        self.rect = pygame.Rect(rect)
        self.rect.x = x
        #pygame.mixer.pre_init(44100, 16, 2, 4096)
        #pygame.init()
        pygame.mixer.Sound.play(pygame.mixer.Sound(path + r'\images\Bosses\Omega\Rings.wav'))
        if y < 50:
            self.rect.y = y+20
        else:
            self.rect.y = y
            self.rect.x = x+5

class Ball(pygame.sprite.Sprite):
    def __init__(self, enemy, incx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path+r'\images\Bosses\Omega\Ball\1.png')
        self.enemy = enemy
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = self.enemy.enemy.rect.x+25
        self.rect.y = self.enemy.enemy.rect.y
        self.down = True
        self.incx = incx
        #pygame.mixer.Sound(path+r'\images\Bosses\Omega\ball.mp3')
        #self.miniball1 = MiniBall(self)
        #self.miniball2 = MiniBall(self)

    def update(self, state):
        if state:
            #self.miniball1.update()
            #self.miniball2.update()
            if self.rect.x > -10 and self.rect.y < 110 and self.down:
                self.rect.x -= self.incx
                self.rect.y +=12
            elif self.rect.x > -10 and self.rect.y > 0 and not self.down:
                self.rect.x -=self.incx
                self.rect.y -=12
            elif self.rect.y >= 110:
                self.down = False
            elif self.rect.y <= 0:
                self.down = True
            elif self.rect.x <= 0:
                self.enemy.ball = None

        if self.rect.x < -10:
            self.enemy.ball = None
            self.enemy.ball2 = None
            #self.miniball1.kill()
            #self.miniball2.kill()
            self.kill()

class MiniBall(pygame.sprite.Sprite):
    def __init__(self, ball):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path + r'\images\Bosses\Omega\Ball\1.png')
        self.ball = ball
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = self.ball.rect.x
        self.rect.y = self.ball.rect.y

    def update(self):
        if self.ball.down:
            self.rect.x -= self.ball.incx+2
            self.rect.y += 5
        else:
            self.rect.x -= self.ball.incx+2
            self.rect.y -= 5

class Boss(Enemy):
    def __init__(self, enemy):
        self.enemy = enemy


    def update(self):
        pass

class Life_Bar(pg.sprite.Sprite):
    def __init__(self, type, w, h, color): #max_life
        pg.sprite.Sprite.__init__(self)
        self.max_life = h#max_life
        #self.life = self.max_life
        self.vissible = False
        self.color = color
        self.w = w
        self.h = h
        #self.rect = pygame.Rect(0, 0, w, h)
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
            #print("P: " + str(self.counter))

    def set_clock(self, clock):
        if self.constant_dmg == 3:
            self.time = clock.tick()
            self.counter += self.time
            #print("E: "+str(self.counter))

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

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, main, color):
        pg.sprite.Sprite.__init__(self)
        self.h = h
        self.w = w
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, self.w, self.h)
        #self.rect = self.image.get_rect()
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