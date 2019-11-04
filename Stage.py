import pygame
from menu import get_screen
from menu import get_screen_object
from menu import get_clock
from Player import *
from Enemy import Enemy
import sys

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        print()

class Stage():
    global world, backdground, backdropbox, player_list

    def __init__(self):
        self.world = get_screen()
        # world = pygame.display.set_mode([worldx, worldy])
        self.backdground = pygame.image.load('images/map1.jpg')#.convert()
        backdropbox = self.world.get_rect()
        self.world.blit(self.backdground, (0, 0))

        # player = Player  # spawn player
        # player.rect.x = 0  # go to x
        # player.rect.y = 0  # go to y
        player_list = pygame.sprite.Group()
        # player_list.add(player)

    def get_background(self):
        return self.backdground

def main():
    file = 'music/stage_1.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.event.wait()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    plataforma1 = Platform(0, 425, 700, 700)
    all_sprites.add(plataforma1)
    platforms.add(plataforma1)

    pygame.key.set_repeat(30)

    jumpCount = 10
    isJump = False

    while 1:
        if megaman.vel.y > 0:
            hits = pygame.sprite.spritecollide(megaman, plataforma1, False)
            if hits:
                megaman.pos.y = hits[0].rect.top
                megaman.vel.y = 0

            megaman.rect.x += 1
            hits = pygame.sprite.spritecollide(megaman, plataforma1, False)
            megaman.rect.x -= 1
            if hits:
                megaman.vel.y = -20
        if (50-10 == 50):
            vel = 25
            fall = 0.005
            while not pygame.sprite.collide_rect(megaman, plataforma1): #TODO SE PETA SI NO ENCUENTRA SUELO NUNCA
                if not isJump:
                    megaman.rect.y -= fall
                    fall -= 0.005
            if not pygame.sprite.collide_rect(megaman, plataforma1):
                megaman.rect.y -= fall
                fall -= 5
            for event in pygame.event.get():
                if not (isJump) and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: #and megaman.speed[1] > vel:
                        megaman.speed[1] = vel

                    #if event.type == pygame.K_DOWN and megaman.speed[1] < 500 - get_screen_object().get_screen_height() - vel:
                        #megaman.speed[1] += vel
                        megaman.rect.y -= vel

                    if event.type == pygame.K_SPACE:
                        megaman.rect.y -= vel
                        isJump = True
                else:
                    if jumpCount >= -10:
                        megaman.speed[1] -= (jumpCount * abs(jumpCount)) * 0.5
                        jumpCount -= 1
                    else:
                        jumpCount = 10
                        isJump = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    #sys.exit()
                # añadimos el evento del teclado
                elif event.type == pygame.KEYDOWN:
                    megaman.update(event)
                    omega.update(event)

        # Main Menu UI
        #filename = 'images/Megaman-background.png'
        # filename = screen.fill((255,255,255))
        #image = pygame.image.load(filename)
        background = stage.get_background()
        get_screen().blit(background, (0, 0))
        get_screen().blit(megaman.img, megaman.rect)
        get_screen().blit(plataforma1.image, plataforma1.rect)
        platforms.draw(get_screen())

        get_clock()
        pygame.display.set_caption("MEGAMAN EXE: STAGE 1")
        pygame.display.flip()
        pygame.display.update()
    # keys=pygame.key.get_pressed()

    # Makes Player character move right by pressing "d"
    # if keys[pygame.K_d]:
    #   x=x+3
    #  if x> 900:
    #     x=900
    # Makes player character move left by pressing "a"
    # if keys[pygame.K_a]:
    #   x=x-3
    #  if x<0:
    #     x=0
    # Makes bullets shoot out of player character by pressing *space*
    # if keys[pygame.K_SPACE]:
    # bullet=Bullet()
    # bullet.rect.x=player.rect.x
    # bullet.rect.y=player.rect.y
    # all_sprites_list.add(bullet)
    # bullet_list.add(bullet)
    # Updates all sprites (makes them move)
    # all_sprites_list.update()
    # Draws all the sprites
    # all_sprites_list.draw(WINDOW)


    world.blit(backdground, backdropbox)
    player_list.draw(world)  # draw player
    pygame.display.flip()
    pygame.display.update()
    menu.get_clock().tick(60)
    pygame.display.set_caption("MEGAMAN EXE: STAGE 1")

stage = Stage()
megaman = Playe()
omega = Enemy()
main()

def get_cosa():
    return "hola"