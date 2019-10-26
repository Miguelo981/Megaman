import pygame
import sys
import os  # new code below


class Player(pygame.sprite.Sprite, width, height):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load('images/MM_WS.png').convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.speed = [15, 15]

        self.rect.centerx = width / 2
        self.rect.centery = height / 2

    def update(self, wait):
        if wait:
            print()#pelota_wilson.rect.midbottom = jugador.rect.midtop
        else:
            if self.rect.top <= 0:  # quitamos que rebote por debajo
                self.speed[1] = -self.speed[1]
            elif self.rect.right >= width or self.rect.left <= 0:
                self.speed[0] = -self.speed[0]
            # movimiento
            self.rect.move_ip(self.speed)
