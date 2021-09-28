import pygame, os
from pygame import *

#Modulo para la preparacion de variables generales del juego
from conf import ASSETS_PATH


def load_map(map):
    f = open(os.path.join(ASSETS_PATH, "maps/"+map+".txt"), "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def change_map(map):
    global game_map
    game_map = load_map(map)

#Menu principal del juego para acceder a las diferentes opciones
def main_menu():
    global lifes, freezeable, points, selected
    menu = True
    selected = "start"
    pygame.init()
    pygame.mixer.stop()
    pygame.mixer.init()
    music(os.path.join(ASSETS_PATH, 'music/main_theme.mp3'), True)
    load_menu()
    static_image = False
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if selected == "controls" and event.key == pygame.K_UP:
                    selected = "start"
                elif selected == "quit" and event.key == pygame.K_UP:
                    selected = "controls"
                if selected == "start" and event.key == pygame.K_DOWN:
                    selected = "controls"
                elif selected == "controls" and event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        static_image = True
                        music(os.path.join(ASSETS_PATH, 'music/megaman-zero-1.mp3'), True)
                        change_map('\map')
                        lifes = 3
                        points = 0
                        freezeable = False
                        import Game
                        Game.init_game()
                    if selected == "controls":
                        static_image = True
                        screen.blit(pygame.image.load(os.path.join(ASSETS_PATH, "images/controls.png")), (0,0))
                    if selected == "quit":
                        pygame.quit()
                        quit()
                if event.key:
                    if not static_image:
                        load_menu()
                    static_image = False
        clock.tick(FPS)
        pygame.display.set_caption("MEGAMAN EXE")
        pygame.display.flip()
        pygame.display.update()

def load_menu():
    global selected

    screen.blit(pygame.image.load(os.path.join(ASSETS_PATH, 'images/Megaman-background3.png')), (0, 0))

    if selected == "start":
        text_start = text_format("START", FONT, 50, WHITE)
    else:
        text_start = text_format("START", FONT, 50, DARK)
    if selected == "controls":
        text_controls = text_format("CONTROLS", FONT, 50, WHITE)
    else:
        text_controls = text_format("CONTROLS", FONT, 50, DARK)
    if selected == "quit":
        text_quit = text_format("QUIT", FONT, 50, WHITE)
    else:
        text_quit = text_format("QUIT", FONT, 50, DARK)

    start_rect = text_start.get_rect()
    controls_rect = text_controls.get_rect()
    quit_rect = text_quit.get_rect()

    screen.blit(text_start, (WIDTH / 1.5 - (start_rect[2] / 2), 300))
    screen.blit(text_controls, (WIDTH / 1.5 - (controls_rect[2] / 2), 400))
    screen.blit(text_quit, (WIDTH / 1.5 - (quit_rect[2] / 2), 500))

def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize).render(message, 0, textColor)
    return newFont

def text_format_pygame(message, textFont, textSize, textColor):
    newFont = pygame.font.SysFont(textFont, textSize).render(message, 0, textColor)
    return newFont

def music(file, state):
    if state:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        pygame.event.wait()
    else:
        pygame.mixer.stop()

path = os.getcwd()
TITLE = "MEGAMAN"
WIDTH = 1200
HEIGHT = 750
FPS = 60
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
ICON = os.path.join(ASSETS_PATH, "images/megaman_exe_navi.png")
FONT = os.path.join(ASSETS_PATH, "fonts/Mega-Man-Battle-Network.ttf")
name = "Megaman"
FPS = 60
lifes = 3
points = 0
freezeable = False

def get_points_text():
    if len(str(points)) > 3:
        return "0" + str(points)
    elif len(str(points)) > 2:
        return "00"+str(points)
    elif len(str(points)) > 1:
        return "000"+str(points)
    if len(str(points)) > 0:
        return "0000"+str(points)


grass_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/grass.png'))
dirt_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/dirt.png'))
metal1_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/m1.png'))
metal2_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/m2.png'))
metal3_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/m3.png'))
path1_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/p1.png'))
path2_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/p2.png'))
path3_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/p3.png'))
path4_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/p4.png'))
roof1_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r1.png'))
roof2_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r2.png'))
roof3_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r3.png'))
roof4_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r4.png'))
roof5_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r5.png'))
roof6_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r6.png'))
roof7_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/r7.png'))
wall1_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w1.png'))
wall2_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w2.png'))
wall3_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w3.png'))
wall4_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w4.png'))
wall5_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w5.png'))
wall6_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w6.png'))
wall7_img = pygame.image.load(os.path.join(ASSETS_PATH, 'images/blocks/w7.png'))
true_scroll = [0,0]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
GOLD = (249, 166, 2)
DARK = (7, 7, 23)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load(ICON))
clock = pygame.time.Clock()
