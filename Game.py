from encodings.punycode import selective_find

import pygame as pg
import pygame
import random

from pygame.tests.base_test import pygame_quit

from moviepy.editor import VideoFileClip
from objects import *
import Settings

#TODO SONIDOS, SONIDO CUANDO CAIGAS

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        change_map('\map')
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #self.screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF)
        #self.screen.set_mode((WIDTH, HEIGHT), flags=pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF)
        self.display = pg.Surface((275, 150)) #300 200
        #self.display.fill((255,255,255))
        #self.background = pygame.image.load("images/bg.jpg")
        #self.display.blit(self.background, (0,0))
        pg.display.set_caption(Settings.TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.vertical_momentum = 0
        self.air_timer = 0
        self.enemies = []
        self.objects = []
        self.doors = []
        self.counter = 0
        self.time = 0
        self.freeze_camera = False
        self.freezeable = False

    def set_enemies(self):
        #self.enemies.append(Omega(Enemy(1155, 10, 100, 143, self), self.player)) #50 155 10 1250
        self.enemies.append(Minion(250, 105, 26, 39, self))
        self.enemies.append(Minion(350, 105, 26, 39, self))
        self.enemies.append(Minion(550, 105, 26, 39, self))
        self.enemies.append(Minion(650, 105, 26, 39, self))
        self.enemies.append(Minion(850, 105, 26, 39, self))
        self.enemies.append(Minion(950, 105, 26, 39, self))
        self.enemies.append(Minion(250, 105, 26, 39, self))
        self.enemies.append(Minion(350, 105, 26, 39, self))
        self.enemies.append(Minion(550, 105, 26, 39, self))
        self.enemies.append(Minion(650, 105, 26, 39, self))
        self.enemies.append(Minion(850, 105, 26, 39, self))
        self.enemies.append(Minion(950, 105, 26, 39, self))

    def get_tile_sprite(self, tile):
        if tile == '1':
            return Settings.dirt_img
        if tile == '2':
            return Settings.grass_img
        if tile == '3':
            return Settings.metal1_img
        if tile == '4':
            return Settings.metal2_img
        if tile == '5':
            return Settings.metal3_img
        if tile == '6':
            return Settings.path1_img
        if tile == '7':
            return Settings.path2_img
        if tile == '8':
            return Settings.path3_img
        if tile == '9':
            return Settings.path4_img
        if tile == 'a':
            return Settings.roof1_img
        if tile == 'b':
            return Settings.roof2_img
        if tile == 'c':
            return Settings.roof3_img
        if tile == 'd':
            return Settings.roof4_img
        if tile == 'l':
            return Settings.roof5_img
        if tile == 'm':
            return Settings.roof6_img
        if tile == 'n':
            return Settings.roof7_img
        if tile == 'e':
            return Settings.wall1_img
        if tile == 'f':
            return Settings.wall2_img
        if tile == 'g':
            return Settings.wall3_img
        if tile == 'h':
            return Settings.wall4_img
        if tile == 'i':
            return Settings.wall5_img
        if tile == 'j':
            return Settings.wall6_img
        if tile == 'k':
            return Settings.wall7_img

    def display_video(self, name):
        clip = VideoFileClip(path + r'/videos/'+name+'.mp4')
        clip.preview()
        #self.movie = pygame.movie.Movie(path + r'/videos/'+name+'.mpeg')
        #self.display = pygame.display.set_mode(self.movie.get_size())
        #movie_screen = pygame.Surface(self.movie.get_size()).convert()
        #self.movie.set_display(self.display)

    def charge_map(self):
        global scroll
        if not self.freeze_camera:
            true_scroll[0] += (self.player.rect.x - true_scroll[0] - 100)  #152
        #true_scroll[1] += (self.player.rect.y - true_scroll[1] - 106)  #106
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
        #scroll[1] = int(scroll[1])
        self.tile_rects = []
        #tile_rects = []
        y = 0
        for layer in Settings.game_map:
            x = 0
            for tile in layer:
                if self.player.rect.x > 100 and tile != '0':
                    self.display.blit(self.get_tile_sprite(tile), (x*16-scroll[0],y*16))
                elif tile != '0':
                    self.display.blit(self.get_tile_sprite(tile), (x * 16, y * 16))
                    scroll[0] = 0
                if tile!= '0':
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                '''if tile == '1':
                    self.display.blit(Settings.dirt_img, (x * 16, y * 16))
                if tile == '2':
                    self.display.blit(Settings.grass_img, (x * 16, y * 16))
                if tile == '3':
                    self.display.blit(Settings.metal1_img, (x * 16, y * 16))
                if tile == '4':
                    self.display.blit(Settings.metal2_img, (x * 16, y * 16))
                if tile == '5':
                    self.display.blit(Settings.metal3_img, (x * 16, y * 16))
                if tile != '0':
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))'''
                #self.all_sprites.add(t)
                #self.platforms.add(t)
                x += 1
            y += 1

        self.player.rect.y += self.vertical_momentum*1.5
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

        collisions = self.move(self.tile_rects)

        if collisions['bottom'] == True and self.player.alive:
            self.air_timer = 0
            self.vertical_momentum = 0
            self.player.air = False
            #self.player.rect.y = 0
        else:
            self.player.air = True
            self.air_timer += 1
            if not self.player.shoot:
                self.player.img = pg.image.load(path + r'\images\Megaman\MM_jump\1.png')

        if self.collision_player_enemy_wall():
            self.player.rect.x = self.player.rect.x-4

        if self.collision_player_enemy():
            pass

        if self.collision_player_rings():
            pass #TODO ADD DMG ANIMATION

        if self.collision_player_ball():
            pass
        if self.collision_player_object():
            pass

        if self.collision_player_door():
            self.enemies.clear()
            self.freeze_camera = True
            scroll[0] = 0
            self.player.rect.x = 10
            Settings.change_map('\map2')
            self.player.able_to_move = False
            self.display_video('warning')
            self.player.able_to_move = True
            self.enemies.append(Omega(Enemy(155 - scroll[0], 10, 100, 143, self), self.player))
            self.all_sprites.add(self.enemies)

            music(path + r'/music/vs_omega.mp3', True)

        if self.player.rect.x > 100:
            self.display.blit(pygame.transform.flip(self.player.img, not self.player.right, False), (self.player.rect.x-scroll[0], self.player.rect.y))
        else:
            self.display.blit(pygame.transform.flip(self.player.img, not self.player.right, False), (self.player.rect.x, self.player.rect.y))
        self.display.blit(pygame.image.load(path+'\images\MM_WS_life_bar.png'), (0,34))
        self.display.blit(self.player.life.background, (self.player.life.rect.x, self.player.life.rect.y))
        self.display.blit(self.player.life.image, (self.player.life.rect.x, self.player.life.rect.y))
        if self.player.charging:
            self.display.blit(pygame.transform.flip(self.player.charge.img, False, False), (self.player.charge.rect.x-scroll[0], self.player.charge.rect.y))
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                if enemy.enemy.life.w > 0:
                    self.display.blit(enemy.enemy.life.image, (enemy.enemy.rect.x + 25, enemy.enemy.rect.y - 10))
                else:
                    enemy.enemy.kill()
                    self.enemies.remove(enemy)
            else:
                if enemy.life.w > 0:
                    self.display.blit(enemy.life.image, (enemy.rect.x-scroll[0], enemy.rect.y - 10))
                elif enemy.rect.y > 121:
                    enemy.kill()
                    self.enemies.remove(enemy)


        #self.display.blit(self.player.img, (self.player.rect.x, self.player.rect.y))
        #self.player.rect = self.move(tile_rects)

    def new(self):
        # start a new game
        self.doors.append(Door(1345, 60, False))
        self.doors.append(Door(1550, 60, True))
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.set_enemies()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemies)
        self.all_sprites.add(self.objects)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.charge_map()
            self.player.set_clock()
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def collision_bullet(self, bullet):
        for tile in self.tile_rects:
            #print(self.player.rect)
            if bullet.rect.colliderect(tile):
                self.tile_rects.remove(tile)
                return True
        return False

    def collision_enemy(self, bullet):
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                if bullet.rect.colliderect(enemy.enemy):
                    if bullet.special:
                        enemy.enemy.life.quit_enemy_life(9)
                        enemy.enemy.life.constant_dmg = 3
                    else:
                        enemy.enemy.life.quit_enemy_life(3)
                    return True
            elif bullet.rect.colliderect(enemy):
                    if bullet.special:
                        enemy.life.quit_minion_life(9)
                        enemy.life.constant_dmg = 3
                    else:
                        enemy.life.quit_minion_life(3)
                    return True
        return False

    def collision_bullet_player(self, bullet):
        if bullet.rect.colliderect(self.player):
            self.player.life.quit_life(3)
            return True
        return False

    def collision_player_enemy(self):
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                if self.player.rect.colliderect(enemy.enemy):
                    self.player.life.quit_life(3)
                    return True
            elif self.player.rect.colliderect(enemy):
                self.player.life.quit_life(3)
                return True
        return False

    def collision_player_enemy_wall(self):
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                if self.player.rect.colliderect(enemy.invisibleWall):
                    return True
        for door in self.doors:
            if door.box != None:
                if self.player.rect.colliderect(door.box):
                    return True
        return False

    def collision_player_rings(self):
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                if enemy.left_hand.ring != None:
                    if self.player.rect.colliderect(enemy.left_hand.ring):
                        self.player.life.quit_life(5)
                        return True
                if enemy.right_hand.ring != None:
                    if self.player.rect.colliderect(enemy.right_hand.ring):
                        self.player.life.quit_life(5)
                        return True
        return False

    def collision_player_ball(self):
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                for ball in enemy.balls:
                    if ball != None and self.player.rect.colliderect(ball):
                        self.player.life.quit_life(5)
                        return True
        return False

    def collision_player_object(self):
        for object in self.objects:
            if object.type != "None":
                if self.player.rect.colliderect(object):
                    object.effect()
                    return True
        return False

    def collision_player_door(self):
        for door in self.doors:
            if self.player.rect.colliderect(door):
                self.freezeable = True
                door.open()
                if door.scene and door.count > 15:
                    return True
            else:
                door.close()
        return False

    def update(self):
        #self.display.blit(pygame.transform.flip(self.player))
        #self.player.spawn()
        # Game Loop - Update
        self.all_sprites.update()
        #print(self.player.rect)
        if self.player.rect.x > 1200 and not self.freezeable:
            self.freeze_camera = True
        else:
            self.freeze_camera = False

        for enemy in self.enemies:
            if not enemy.__class__.__name__ == "Omega":
                for bullet in enemy.shoots:
                    bullet.update()
                    if bullet.active:
                        self.display.blit(pygame.transform.flip(bullet.img, not bullet.right, False), (bullet.rect.x - scroll[0], bullet.rect.y))
                        if self.collision_bullet(bullet) or self.collision_bullet_player(bullet):
                            bullet.active = False
                    else:
                        enemy.shoots.remove(bullet)
                enemy.set_clock()

        for bullet in self.player.shoots:
            bullet.update()
            if bullet.active:
                self.display.blit(pygame.transform.flip(bullet.img, not bullet.right, False), (bullet.rect.x-scroll[0], bullet.rect.y))
                if self.collision_bullet(bullet):
                    bullet.active = False
                if self.collision_enemy(bullet):
                    bullet.active = False
            else:
                self.player.shoots.remove(bullet)

        self.player.collide = False
        if self.player.rect.y > Settings.HEIGHT - 200:
            self.player = Player(self)
            self.all_sprites.add(self.player)
            Settings.lifes -= 1

    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            #print(self.player.rect)
            if self.player.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def collision_test_object(self, object, tiles):
        hit_list = []
        for tile in tiles:
            if  object.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        #self.player.rect.x += self.player.vel.x
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.player.vel.x > 0:
                self.player.rect.right = tile.left
                collision_types['right'] = True
            elif self.player.vel.x < 0: #movement[0] < 0
                self.player.rect.left = tile.right
                collision_types['left'] = True
        self.player.rect.y += 3
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.player.vel.y > 0:
                self.player.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.player.vel.y < 0:
                self.player.rect.top = tile.bottom
                collision_types['top'] = True
        return collision_types

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if self.player.alive:
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_a:
                        self.player.rect = pygame.Rect(self.player.rect.x,self.player.rect.y-10,15,34)
                    if event.key == pg.K_z and self.player.shoot:
                        if self.player.counter > 350:
                            bullet = Bullet(self.player)
                            bullet.special = True
                            self.player.shoots.append(bullet)
                            self.player.charging = False
                        else:
                            self.player.shoots.append(Bullet(self.player))
                            self.player.shoot = False
                            self.player.charging = False
                            #self.player.sound.stop()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        if self.player.counter > 100:
                            self.player.charging = True
                            #self.player.sound.play(pygame.mixer.Sound(path + r'\images\ROCK_X5_00183.wav'))
                        self.player.shoot = True
                        self.player.counter = 0
                    if event.key == pg.K_SPACE:
                        if self.air_timer < 6:
                            self.vertical_momentum = -5
                        #self.player.jump()
            else:
                music(path+r'/music/vs_omega.mp3', False)
                if event.key:
                    import Settings
                    Settings.main_menu()
            self.counter += self.time

    def draw(self):
        # Game Loop - draw
        #self.screen.fill(BLACK)
        #self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        screen.blit(pygame.transform.scale(self.display, (Settings.WIDTH, Settings.HEIGHT)), (0, 0))
        '''pygame.draw.rect(self.display, (7, 80, 75), pygame.Rect(Settings.WIDTH, Settings.HEIGHT, Settings.WIDTH, Settings.HEIGHT))
        pg.draw.rect(self.display, (255, 255, 255), pg.Rect(0, 0, Settings.WIDTH, Settings.HEIGHT))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0] - self.player.rect.x * background_object[0],
                                   background_object[1][1] - self.player.rect.y * background_object[0], background_object[1][2],
                                   background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(self.display, (14, 222, 150), obj_rect)
            else:
                pygame.draw.rect(self.display, (9, 91, 85), obj_rect)'''
        #image = pygame.transform.scale(pg.image.load(path + r'\images\Bosses\Omega\vsOmega.png'), (300, 200))
        #pygame.draw.rect(self.display, pg.image.load(path + r'\images\Bosses\Omega\vsOmega.png'), pg.Rect(self.player.rect.x *0.5, self.player.rect.y * 0.5, 276, 159))
        #image = pg.image.load(path + r'\images\Bosses\Omega\vsOmega.png')
        image = pg.image.load(path + r'\images\maps\background1.png')
        #pillar = pg.image.load(path + r'\images\maps\pillars.png')

        self.display.blit(image, pg.Rect(-self.player.rect.x * 0.4, (self.player.rect.y * 0.1)-11, 276, 159))
        #self.display.blit(pillar, pg.Rect(-self.player.rect.x * 0.05, (self.player.rect.y * 0.1)-11, 276, 159))

        self.display.blit(Settings.text_format_pygame(Settings.get_points_text(), "consolas", 12, WHITE), (3, 20))
        self.display.blit(Settings.text_format_pygame(str(Settings.lifes), "consolas", 10, WHITE), (5, 95))
        #self.display.blit(Settings.text_format(str(Settings.lifes), FONT, 6, WHITE), (6, 95))
        for door in self.doors:
            door.update()
            self.display.blit(door.img, (door.rect.x-scroll[0], door.rect.y))

        for object in self.objects:
            if object.type != "None":
                object.update()
                object.rect.y += object.vertical_momentum * 1.5
                object.vertical_momentum += 0.2
                if object.vertical_momentum > 3:
                    object.vertical_momentum = 3

                for tile in self.collision_test_object(object, self.tile_rects):
                    object.rect.y += 3
                    if self.player.vel.y > 0:
                        object.rect.bottom = tile.top
                        object.vertical_momentum = 0
                self.display.blit(pygame.transform.flip(object.img, False, False),(object.rect.x-scroll[0], object.rect.y))

        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Omega":
                self.display.blit(pygame.transform.flip(enemy.left_hand.img, enemy.left_hand.left, False),(enemy.left_hand.rect.x, enemy.left_hand.rect.y))
                self.display.blit(pygame.transform.flip(enemy.enemy.img, not enemy.enemy.right, False), (enemy.enemy.rect.x, enemy.enemy.rect.y))
                self.display.blit(pygame.transform.flip(enemy.right_hand.img, False, False),(enemy.right_hand.rect.x, enemy.right_hand.rect.y))
                if enemy.left_hand.ring != None:
                    self.display.blit(pygame.transform.flip(enemy.left_hand.ring.img, not enemy.enemy.right, False), (enemy.left_hand.ring.rect.x, enemy.left_hand.ring.rect.y))
                if enemy.right_hand.ring != None:
                    self.display.blit(pygame.transform.flip(enemy.right_hand.ring.img, False, False), (enemy.right_hand.ring.rect.x, enemy.right_hand.ring.rect.y))
                for ball in enemy.balls:
                    if ball.active != None:
                        self.display.blit(pygame.transform.flip(ball.image, False, False), (ball.rect.x, ball.rect.y))
                #if enemy.ball2 != None:
                    #self.display.blit(pygame.transform.flip(enemy.ball2.image, False, False), (enemy.ball2.rect.x, enemy.ball2.rect.y))
                    #self.display.blit(pygame.transform.flip(enemy.ball.miniball1.image, False, False), (enemy.ball.miniball1.rect.x, enemy.ball.miniball1.rect.y))
                    #self.display.blit(pygame.transform.flip(enemy.ball.miniball2.image, False, False), (enemy.ball.miniball2.rect.x, enemy.ball.miniball2.rect.y))
            else:
                self.display.blit(pygame.transform.flip(enemy.img, not enemy.right, False),(enemy.rect.x-scroll[0], enemy.rect.y))


        #pg.image.load('images/bg.jpg')
        #screen.blit(self.player.image, (WIDTH/2,HEIGHT/2))
        #self.display.blit(pygame.transform.scale(self.display, (WIDTH, HEIGHT)), (0, 0))
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

def init_game():
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()
    pygame.quit()