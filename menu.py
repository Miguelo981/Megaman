import time
import pygame
import os


def init_game_settings():
    global screen, text_format, white, black, gray, red, green, blue, yellow, font, screen_width, clock, FPS
    # Game Initialization
    pygame.init()

    # Center the Game Application
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Game Resolution
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

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

    # Game Fonts
    font = "fonts/Mega-Man-Battle-Network.ttf"

    # Game Framerate
    clock = pygame.time.Clock()
    FPS = 30

def start_window():
    global pantalla
    width = 800
    higth = 600
    color_negro_fondo = (0, 0, 0)
    color_blanco = (255, 255, 255)
    pygame.init()

    pantalla = pygame.display.set_mode((width, higth))
    pygame.display.set_caption("Megaman")


def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        print("Start")
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(blue)
        title = text_format("Sourcecodester", font, 90, yellow)
        if selected == "start":
            text_start = text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")


def start_menu():
    start_window()
    # reloj para medir la velocidad
    reloj = pygame.time.Clock()
    # ajustamos la repetición de la tecla pulsada
    pygame.key.set_repeat(30)
    puntuacion = 0  # agregamos la puntuacion
    vidas = 3  # agregamos vidas al jugador


def get_pantalla():
    return pantalla

init_game_settings()
main_menu()
start_menu()
