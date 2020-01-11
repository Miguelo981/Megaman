import pygame, sys, os

def main_menu():
    menu = True
    selected = "start"

    pygame.init()
    ###song = 'music/main_theme.mp3'
    #music(song, True)
    pygame.mixer.init()

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
                        print("Start")
                        music(path+r'/music/vs_omega.mp3', True)
                        #####music(song, False)
                        #import Stage
                        #####music('music/stage_1.mp3', True)
                        import Game
                        Game.init_game()
                    if selected == "controls":
                        print("Controls")
                        #stage = Stage()
                    if selected == "quit":
                        pygame.quit()
                        quit()
            if event.type == pygame.QUIT:
                sys.exit()
            # añadimos el evento del teclado
            #elif event.type == pygame.KEYDOWN:
                #megaman.update(event)

        # Main Menu UI
        filename = path+'/images/Megaman-background2.png'
        #filename = screen.fill((255,255,255))
        image = pygame.image.load(filename)
        screen.blit(image, (0,0))

        #megaman = Player()
        #screen.blit(megaman.img, megaman.rect)

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

        # Main Menu Text
        screen.blit(text_start, (WIDTH / 1.5 - (start_rect[2] / 2), 200))
        screen.blit(text_controls, (WIDTH / 1.5 - (controls_rect[2] / 2), 300))
        screen.blit(text_quit, (WIDTH / 1.5 - (quit_rect[2] / 2), 400))

        clock.tick(FPS)
        pygame.display.set_caption("MEGAMAN EXE")
        pygame.display.flip()
        pygame.display.update()

def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText

def music(file, state):
    if state:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        pygame.event.wait()
    else:
        pygame.mixer.stop()

# game options/settings
path = os.getcwd()
TITLE = "MEGAMAN"
'''WIDTH = 1000
HEIGHT = 700'''
WIDTH = 800 #500,350,       600, 400, 800, 500
HEIGHT = 500
FPS = 60

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
ICON = path+"/images/megaman_exe_navi.png"
FONT = path+"/fonts/Mega-Man-Battle-Network.ttf"
name = "\Megaman"
FPS = 60

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

grass_img = pygame.image.load(path+'/images/blocks/grass.png')
dirt_img = pygame.image.load(path+'/images/blocks/dirt.png')
metal1_img = pygame.image.load(path+'/images/blocks/m1.png')
metal2_img = pygame.image.load(path+'/images/blocks/m2.png')
metal3_img = pygame.image.load(path+'/images/blocks/m3.png')
#background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
true_scroll = [0,0]

# define colors
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
