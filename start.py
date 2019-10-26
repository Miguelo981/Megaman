import pygame, sys
from pygame.locals import *

while 1:
    import menu
    menu.init_game_settings()
    menu.main_menu()

pygame.init()
screen = pygame.display.set_mode((400,400),0,32)
myFont = pygame.font.SysFont('arial', 14)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    x,y = pygame.mouse.get_pos()
    label = myFont.render('mouse coords: ' + str(x) + ', ' + str(y), 1, (0,128,255))

    screen.blit(label, (10,10))
    pygame.display.update()

while 1:
    import menu
    menu.init_game_settings()
    menu.main_menu()