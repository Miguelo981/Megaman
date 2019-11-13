import pygame as pg
import random
from Settings import *
from objects import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.player.set_clock()
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            #hits = pg.sprite.collide_rect(self.player, self.platforms)
            if hits:
                if hits[0].main:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                elif self.player.rect.y <= hits[0].rect.y and not hits[0].main:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    #print("choquearri")
                if (self.player.rect.top < hits[0].rect.y) and not hits[0].main: #or self.player.rect.top <= hits[0].rect.bottom
                    #self.player.rect.top = hits[0].rect.y + self.player.rect.y
                    #self.player.rect.top = hits[0].rect.bottom
                    #self.player.rect.top = hits[0].rect.y + 5
                    #self.player.rect.y = hits[0].rect.bottom + 5
                    self.player.collide = True
                    print("coqueba")
                print(self.player.collide)
                '''if self.player.rect.y >= hits[0].rect.y and not hits[0].main:
                        self.player.pos.y = hits[0].rect.bottom #TODO CALCULAR DIFERENCIA
                        print("coqueba")'''
                if self.player.rect.x <= hits[0].rect.x and self.player.pos.y != hits[0].rect.top and not hits[0].main:
                    #self.player.pos.x = hits[0].rect.x
                    self.player.pos.x = hits[0].rect.left
                    self.player.vel.x = 0
                    print("choqueiz")
                if self.player.rect.x >= hits[0].rect.x and self.player.pos.y != hits[0].rect.top and not hits[0].main:
                    #self.player.pos.x = hits[0].rect.x + hits[0].w
                    self.player.pos.x = hits[0].rect.right
                    self.player.vel.x = 0
                    print("choquede")
                '''keys = pg.key.get_pressed()
                    if keys[pg.K_RIGHT]:
                        self.player.pos.x -= 2
                    elif keys[pg.K_LEFT]:
                        self.player.pos.x += 2
                if hits[0].rect.y == self.player.rect.y or self.player.pos.y <= hits[0].rect.y + hits[0].rect.h and not hits[0].main:
                    #print(hits[0].rect.y)
                    #print(hits[0].rect.h)
                    #print(self.player.rect.y) #self.player.rect.y
                    self.player.pos.y = hits[0].rect.y + hits[0].rect.h
                    self.player.vel.y = 0
                #if hits[0].rect.y <= self.player.rect.y <= hits[0].rect.y + hits[0].rect.h and not hits[0].main:
                    #self.player.pos.y = hits[0].rect.h + hits[0].rect.y
                    #self.player.vel.y = 0
                    #print("sorpresa")
                if self.player.pos.y == hits[0].rect.bottom:
                    self.player.pos.y = hits[0].rect.bottom
                    self.player.vel.y = 0
                    print("debajo")
                if self.player.pos.y == hits[0].rect.top:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
            for hit in hits:
                self.player.vel.y = 0  ##si pones eso en caida, arenas movedizas
                print(hit)
                if self.player.pos.y == hit.rect.top:
                    print("encima")
                    self.player.pos.y = hit.rect.top
                    self.player.vel.y = 0
                if self.player.pos.y == hit.rect.bottom:
                    self.player.pos.y = hit.rect.bottom
                    #print("estas encima")
                    self.player.vel.y = 0
                    print(hit.rect.bottom)
                if self.player.pos.y == hits[0].rect.top:
                    print("encima")
                if self.player.pos.y == hits[0].rect.bottom:
                    print("hola")'''
                    #self.player.pos.y = hits[0].rect.top - hits[0].h
                    #self.player.vel.y = 0
                #self.player.pos.y = hits[0].rect.top
                #self.player.vel.y = 0
                #print(self.player.pos.y)
        self.player.collide = False
        if self.player.pos.y > HEIGHT:
            self.player.pos = vec(WIDTH / 2, HEIGHT / 2)
            #self.player.kill()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
