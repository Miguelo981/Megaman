import pygame
import menu
import Player

class Stage():
    global world, backdground, backdropbox, player_list

    world = menu.get_screen()
    #world = pygame.display.set_mode([worldx, worldy])
    backdground = pygame.image.load('images/map1.jpg').convert()
    backdropbox = world.get_rect()
    world.blit(backdground, (0, 0))

    #player = Player  # spawn player
    #player.rect.x = 0  # go to x
    #player.rect.y = 0  # go to y
    player_list = pygame.sprite.Group()
    #player_list.add(player)

while 1:
    keys=pygame.key.get_pressed()

    #Makes Player character move right by pressing "d"
    if keys[pygame.K_d]:
        x=x+3
        if x> 900:
            x=900
    #Makes player character move left by pressing "a"
    if keys[pygame.K_a]:
        x=x-3
        if x<0:
            x=0
    #Makes bullets shoot out of player character by pressing *space*
    #if keys[pygame.K_SPACE]:
        #bullet=Bullet()
        #bullet.rect.x=player.rect.x
        #bullet.rect.y=player.rect.y
        #all_sprites_list.add(bullet)
        #bullet_list.add(bullet)
#Updates all sprites (makes them move)
    #all_sprites_list.update()
#Draws all the sprites
    #all_sprites_list.draw(WINDOW)


    world.blit(backdground, backdropbox)
    player_list.draw(world)  # draw player
    pygame.display.flip()
    pygame.display.update()
    menu.get_clock().tick(60)
    pygame.display.set_caption("MEGAMAN EXE: STAGE 1")