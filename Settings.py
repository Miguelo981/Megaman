import pygame
import sys

def main_menu():
    menu = True
    selected = "start"

    pygame.init()
    song = 'music/main_theme.mp3'
    #music(song, True)
    #pygame.mixer.init()

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
                        #######music(song, False)
                        #import Stage
                        ########music('music/stage_1.mp3', True)
                        import Game
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
        filename = 'images/Megaman-background.png'
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
        screen.blit(text_start, (WIDTH / 1.5 - (start_rect[2] / 2), 300))
        screen.blit(text_controls, (WIDTH / 1.5 - (controls_rect[2] / 2), 400))
        screen.blit(text_quit, (WIDTH / 1.5 - (quit_rect[2] / 2), 500))

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
TITLE = "MEGAMAN"
WIDTH = 1000
HEIGHT = 700
FPS = 60

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
ICON = "images/megaman_exe_navi.png"
FONT = "fonts/Mega-Man-Battle-Network.ttf"
FPS = 60

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH / 1.5, 40, True),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20, False),
                 (125, HEIGHT - 350, 100, 20, False),
                 (350, 200, 100, 20, False),
                 (175, 100, 50, 20, False),
                 (300, 500, 70, 50, False),
                 (600, 600, 60, 120, False)]

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
