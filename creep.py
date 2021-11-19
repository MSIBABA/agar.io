import random

import pygame
from pygame.math import Vector2


class Creep:
    def __init__(self):
        self.pos = Vector2(random.randint (800,800))
        self.taille = 10
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.masse = 10

    def show (self,screen):
        pygame.draw.circle(screen,self.color,[int(self.pos.x),int(self.pos.y)],self.taille)
