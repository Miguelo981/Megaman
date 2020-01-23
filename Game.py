from moviepy.editor import VideoFileClip
from objects import *
import Settings


class Game:
    def __init__(self):
        pg.init()
        change_map('\map')
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.display = pg.Surface((275, 150))
        pg.display.set_caption(TITLE)
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
        self.pause = False
        self.gameover = False

    def set_enemies(self):
        #self.enemies.append(Omega(Enemy(155, 10, 100, 143, self), self.player)) #50 155 10 1250
        self.enemies.append(Minion(250, 105, 26, 39, self))
        self.enemies.append(Minion(350, 105, 26, 39, self))
        self.enemies.append(Minion(550, 105, 26, 39, self))
        self.enemies.append(Minion(650, 105, 26, 39, self))
        self.enemies.append(Minion(850, 105, 26, 39, self))
        self.enemies.append(Minion(900, 105, 26, 39, self))
        self.enemies.append(Minion(450, 105, 26, 39, self))
        self.enemies.append(Minion(750, 105, 26, 39, self))
        self.enemies.append(Minion(500, 105, 26, 39, self))
        self.enemies.append(Minion(600, 105, 26, 39, self))
        self.enemies.append(Minion(1250, 105, 26, 39, self))
        self.enemies.append(Minion(1200, 105, 26, 39, self))

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
        clip.size = (1200, 750)
        clip.preview()

    def charge_map(self):
        global scroll
        if not self.freeze_camera and not Settings.freezeable:
            true_scroll[0] += (self.player.rect.x - true_scroll[0] - 100)
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
        self.tile_rects = []
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
                x += 1
            y += 1

        if not self.pause:
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
                pass

            if self.collision_player_ball():
                pass
            if self.collision_player_object():
                pass

            if self.collision_player_door():
                self.enemies.clear()
                self.freeze_camera = True
                scroll[0] = 0
                self.player.rect.x = 10
                change_map('\map2')
                self.player.able_to_move = False
                self.display_video('warning2')
                self.player.able_to_move = True
                self.enemies.append(Omega(Enemy(155 - scroll[0], 10, 100, 143, self), self.player))
                self.all_sprites.add(self.enemies)
                Settings.freezeable = True
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
                    self.gameover = True
                    self.pause = True
                    enemy.enemy.kill()
                    self.enemies.remove(enemy)
            else:
                if enemy.life.w > 0:
                    self.display.blit(enemy.life.image, (enemy.rect.x-scroll[0], enemy.rect.y - 10))
                elif enemy.rect.y > 121:
                    enemy.kill()
                    self.enemies.remove(enemy)

    def new(self):
        # start a new game
        self.doors.append(Door(1345, 60, True))
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
        self.playing = True
        while self.playing:
            self.charge_map()
            self.player.set_clock()
            self.clock.tick(FPS)
            self.events()
            if not self.pause:
                self.update()
            self.draw()

    def collision_bullet(self, bullet):
        for tile in self.tile_rects:
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
                    if ball != None and ball.active and self.player.rect.colliderect(ball):
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
                door.open()
                self.freeze_camera = False
                Settings.freezeable = True
                if door.scene and door.count > 15:
                    return True
            else:
                door.close()
        return False

    def update(self):
        self.all_sprites.update()
        if self.player.rect.x > 1200 and not Settings.freezeable:
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
        if self.player.rect.y > HEIGHT - 300 and self.player.alive and not Settings.lifes < 1:
            self.player.life.h = 0
            self.player.death()
        if self.player.rect.y < 0:
            self.player.rect.y += 100

        if Settings.lifes < 1:
            self.pause = True
            self.gameover = True
            music(path+r'/music/vs_omega.mp3', False)

        elif not self.player.alive:
            self.player = Player(self)
            self.all_sprites.add(self.player)

    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
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
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.player.vel.x > 0:
                self.player.rect.right = tile.left
                collision_types['right'] = True
            elif self.player.vel.x < 0:
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
        for event in pg.event.get():
            if self.player.alive:
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYUP and not self.pause:
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
                    if event.key == pg.K_ESCAPE:
                        main_menu()
                    if event.key == pg.K_RETURN:
                        self.pause = not self.pause
                    if event.key == pg.K_z:
                        if self.player.counter > 100:
                            self.player.charging = True
                            #self.player.sound.play(pygame.mixer.Sound(path + r'\images\ROCK_X5_00183.wav'))
                        self.player.shoot = True
                        self.player.counter = 0
                    if event.key == pg.K_SPACE:
                        if self.air_timer < 6:
                            self.vertical_momentum = -5
            elif self.pause and self.gameover:
                if event.key:
                    main_menu()
            self.counter += self.time

    def draw(self):
        screen.blit(pygame.transform.scale(self.display, (WIDTH, HEIGHT)), (0, 0))
        image = pg.image.load(path + r'\images\maps\background1.png')
        self.display.blit(image, pg.Rect(-self.player.rect.x * 0.4, (self.player.rect.y * 0.1)-11, 276, 159))
        self.display.blit(text_format_pygame(get_points_text(), "consolas", 12, WHITE), (3, 20))
        self.display.blit(text_format_pygame(str(Settings.lifes), "consolas", 10, WHITE), (5, 95))

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
                    if ball.active:
                        self.display.blit(pygame.transform.flip(ball.image, False, False), (ball.rect.x, ball.rect.y))
                #if enemy.ball2 != None:
                    #self.display.blit(pygame.transform.flip(enemy.ball2.image, False, False), (enemy.ball2.rect.x, enemy.ball2.rect.y))
                    #self.display.blit(pygame.transform.flip(enemy.ball.miniball1.image, False, False), (enemy.ball.miniball1.rect.x, enemy.ball.miniball1.rect.y))
                    #self.display.blit(pygame.transform.flip(enemy.ball.miniball2.image, False, False), (enemy.ball.miniball2.rect.x, enemy.ball.miniball2.rect.y))
            else:
                self.display.blit(pygame.transform.flip(enemy.img, not enemy.right, False),(enemy.rect.x-scroll[0], enemy.rect.y))
        if self.pause and not self.gameover:
            self.display.blit(text_format_pygame("PAUSE", "consolas", 75, WHITE), (40, 50))
        if self.gameover:
            self.display.blit(text_format_pygame("GAME OVER", "consolas", 50, WHITE), (20, 35))
            self.display.blit(text_format_pygame("PRESS ANY KEY TO RESTART", "consolas", 15, WHITE), (40, 80))
        pg.display.flip()

def init_game():
    g = Game()
    while g.running:
        g.new()
    pygame.quit()