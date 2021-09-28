import random

import pygame as pg
from game.Settings import *

from conf import ASSETS_PATH
from game.entities.objects import InivisbleWall, Life_Bar, load_images


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/main.png'))
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
                self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/main.png'))
            else:
                self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/damage.png'))
            self.life.inmunity()
        else:
            self.img = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/main.png'))

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

#Objeto Omega, boss principal del juego
class Omega(pg.sprite.Sprite):
    def __init__(self, enemy, player):
        pg.sprite.Sprite.__init__(self)
        self.enemy = enemy
        self.left_hand = Left_hand(self.enemy.rect.x, self.enemy.rect.y, player)
        self.right_hand = Right_hand(self.enemy.rect.x, self.enemy.rect.y, player)
        self.balls = []
        self.ball1 = True
        self.ball2 = True
        self.invisibleWall = InivisbleWall(self.enemy.rect.x+20, self.enemy.rect.y, 100, 143)

    def update(self):
        self.enemy.update()
        self.left_hand.update(self.enemy)
        self.right_hand.update(self.enemy)
        for ball in self.balls:
            if ball.active:
                ball.update(True)
        if self.enemy.life.constant_dmg == 3:
            self.enemy.assault = True
            self.left_hand.attack()
            if self.enemy.life.w < 60:
                self.right_hand.attack()
            if self.enemy.life.w < 70 and self.ball1:
                self.balls.append(Ball(self, random.randint(1,6)))
                self.ball1 = False
            if self.enemy.life.w < 30 and not self.ball1 and self.ball2:
                self.balls.append(Ball(self, random.randint(1, 6)))
                self.ball2 = False
            if self.enemy.life.w <= 0:
                self.enemy.game.gameover = True
        else:
            self.ball1 = True
            self.ball2 = True
        if self.left_hand.rings_number == 3 or self.right_hand.rings_number == 3:
            self.enemy.assault = False


class Left_hand(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        pg.sprite.Sprite.__init__(self)
        self.base = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/left_hand.png'))
        self.open = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/hand_open.png'))
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
        self.rings = load_images(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/V_Rings'))
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

class Right_hand(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        pg.sprite.Sprite.__init__(self)
        self.base = pg.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/right_hand.png'))
        self.open = pg.image.load(os.path.join(ASSETS_PATH,'images/Bosses/Omega/r_open.png'))
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
        self.rings = load_images(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/Ring'))
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

#Objeto anillo dispadarado por las manos de Omega
class Ring(pg.sprite.Sprite):
    def __init__(self, x, y, rect):
        pg.sprite.Sprite.__init__(self)
        self.img = None
        self.rect = pygame.Rect(rect)
        self.rect.x = x
        pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/Rings.wav')))
        if y < 50:
            self.rect.y = y+20
        else:
            self.rect.y = y
            self.rect.x = x+5

class Ball(pygame.sprite.Sprite):
    def __init__(self, enemy, incx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/Ball/1.png'))
        self.enemy = enemy
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = self.enemy.enemy.rect.x+25
        self.rect.y = self.enemy.enemy.rect.y
        self.down = True
        self.incx = incx
        self.active = True
        #pygame.mixer.Sound(path+r'\images\Bosses\Omega\ball.mp3')

    def update(self, state):
        if state:
            if random.randint(1,2) == 1:
                self.image = pygame.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/Ball/4.png'))
            else:
                self.image = pygame.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/Ball/1.png'))
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
                self.active = False

        if self.rect.x < -10:
            self.active = False
            self.kill()
            self.enemy.balls.remove(self)

class MiniBall(pygame.sprite.Sprite):
    def __init__(self, ball):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ASSETS_PATH, 'images/Bosses/Omega/Ball/1.png'))
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