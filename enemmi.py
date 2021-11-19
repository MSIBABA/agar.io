import random

from pygame.math import Vector2



class ennemie:
    def __init__(self):
        self.pos = Vector2(random.randint (800,800))
        self.taille = 50
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.masse = 40
        self.Vmax =  50
        self.Acc = 10
        self.Vmin = 5





















