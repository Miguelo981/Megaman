import time
import pygame

def start_window():
    global pantalla
    width = 800
    higth = 600
    color_negro_fondo = (0, 0, 0)
    color_blanco = (255, 255, 255)
    pygame.init()

    pantalla = pygame.display.set_mode((width, higth))
    pygame.display.set_caption("Megaman")

def start_menu():
    start_window()
    #reloj para medir la velocidad
    reloj = pygame.time.Clock()
    #ajustamos la repetición de la tecla pulsada
    pygame.key.set_repeat(30)
    puntuacion = 0 #agregamos la puntuacion
    vidas = 3 #agregamos vidas al jugador

def get_pantalla():
    return pantalla

start_menu()