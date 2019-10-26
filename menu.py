import time
import pygame
import os
from Game_Screen import Game_Screen


def init_game_settings():
    global screen, screen_object, text_format, white, black, gray, red, green, blue, yellow, gold, dark, font, screen_width, screen_height, clock, FPS
    # Game Initialization
    pygame.init()

    screen_object = Game_Screen(700, 1000)
    screen = pygame.display.set_mode((screen_object.get_screen_width(), screen_object.get_screen_height()))

    # Center the Game Application
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    #screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_icon(pygame.image.load("images/megaman_exe_navi.png"))

    # Text Renderer
    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)

        return newText

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (50, 50, 50)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    gold = (249, 166, 2)
    dark = (7, 7, 23)

    # Game Fonts
    font = "fonts/Mega-Man-Battle-Network.ttf"

    # Game Framerate
    clock = pygame.time.Clock()
    FPS = 60

#TODO MIRAR ARKANOID Y HACER DIALOGOS!!

def main_menu():
    menu = True
    selected = "start"

    file = 'music/main_theme.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.event.wait()

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
                    if selected == "controls":
                        import Stage
                        stage = Stage
                    if selected == "quit":
                        pygame.quit()
                        quit()
        # Main Menu UI
        filename = 'images/Megaman-background.png'
        image = pygame.image.load(filename)
        screen.blit(image, (0,0))
        pygame.display.update()

        if selected == "start":
            text_start = text_format("START", font, 50, white)
        else:
            text_start = text_format("START", font, 50, dark)
        if selected == "controls":
            text_controls = text_format("CONTROLS", font, 50, white)
        else:
            text_controls = text_format("CONTROLS", font, 50, dark)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 50, white)
        else:
            text_quit = text_format("QUIT", font, 50, dark)

        start_rect = text_start.get_rect()
        controls_rect = text_controls.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(text_start, (screen_object.get_screen_width() / 1.5 - (start_rect[2] / 2), 300))
        screen.blit(text_controls, (screen_object.get_screen_width() / 1.5 - (controls_rect[2] / 2), 400))
        screen.blit(text_quit, (screen_object.get_screen_width() / 1.5 - (quit_rect[2] / 2), 500))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("MEGAMAN EXE")

def get_screen():
    return screen#pygame.display.set_mode((screen_width, screen_height))

def get_screen_object():
    return get_screen_object()