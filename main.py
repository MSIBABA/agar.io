import random

import pygame
import pygame
from pygame.math import Vector2

import core


def setup():

    print("-------START--------")
    core.fps = 20
    core.WINDOW_SIZE = [800,800]

    #creation creep
    from creep import Creep


    print("---------END--------")

def run():

   core.cleanScreen()
   #afficher creep
   pygame.draw.circle(core.memory("Creep"))








core.main(setup, run)