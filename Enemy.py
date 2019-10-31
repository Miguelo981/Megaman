import pygame
import sys
import menu
import os  # new code below


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.img = pygame.image.load('images/omega.png')  # .convert()
        # self.images.append(self.img)
        # self.image = self.images[0]
        self.rect = self.img.get_rect()  # image
        self.rect.midbottom = (menu.screen_object.get_screen_width() / 1.5, menu.screen_object.get_screen_height() / 1.5)
        #self.rect.midbottom = (menu.screen_object.get_screen_width() / 2, menu.screen_object.get_screen_height() - 20)
        self.speed = [15, 15]

        #self.rect.centerx = menu.screen_object.get_screen_width() / 2
        #self.rect.centery = menu.screen_object.get_screen_height() / 2

    def update(self, evento):

        #self.acc = speed[0, 0.5]
        #buscar si se ha pulsado flecha izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0: #añadimos que no pase del borde derecho
            #print("Me estoy moviendo a la izquierda")
            self.speed = [-10, 0]
        #buscar si se ha pulsado flecha derecha
        elif evento.key == pygame.K_RIGHT and self.rect.right < menu.screen_object.get_screen_width(): #añadimos que no pase del borde izquierdo
            #print("Me estoy moviendo a la derecha")
            self.speed = [10, 0]
        elif evento.key == pygame.K_BACKSPACE:
            self.speed = [0, 10]
        else:
            #print("Me me muevo")
            self.speed = [0, 0]
        #Mover en base a posición actual y velocidad
        self.rect.move_ip(self.speed)

        pygame.display.update()

    def addSpriteImage(sprite, image):
        sprite.addImage(image)