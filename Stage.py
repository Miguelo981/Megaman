import pygame
import menu

class Stage():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
    screen = menu.get_screen()
    pygame.display.set_caption("Megaman")