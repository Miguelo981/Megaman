import time
import pygame
import menu

ANCHO = 800
ALTO = 600
color_negro_fondo = (0,0,0) #color de fondo
color_blanco = (255,255,255) #color del texto
pygame.init()

def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Arial', 20, 0, 0)
    texto = fuente.render(str(puntuacion).zfill(5,), True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0,0]
    menu.get_pantalla().blit(texto, texto_rect)

def mostrar_vidas():
    fuente = pygame.font.SysFont('Arial', 20, 0, 0)
    texto_vidas = 'Vidas: ' + str(vidas).zfill(2)
    texto = fuente.render(texto_vidas, True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topright = [ANCHO,0]
    menu.get_pantalla().blit(texto, texto_rect)

puntuacion = 0
vidas = 3
menu.start_window()