import pygame
import sys
import os # new code below

class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load('images/MM_WS.png').convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect  = self.image.get_rect()