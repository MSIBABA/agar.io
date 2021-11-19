import inspect
import sys
import time
from typing import cast
from types import FrameType

import pygame

screenCleen = True
runfuntion = None
setupfunction = None
screen = None
fps = 60
loopLock = False
WINDOW_SIZE = [100, 100]
width = 0
height = 1
mouseclickleft = None
mouseclickL = False
mouseclickright = [-1, -1]
mouseclickR = False
keyPress = False
keyPressValue = None
keyReleaseValue = None
keyPressList = None
memoryStorage = {}


def printMemory():
    print("--------------MEMORY:-------------------")
    for k, v in memoryStorage.items():
        print("Nom : ", k, " Valeur :", v, " Type : ", type(v))
    print("----------------------------------------")
    print("\n")


def memory(key, value=None):
    global memoryStorage
    if " " in key:
        sys.stderr.write("ERREUR : Espace interdit dans les noms de variable : " + key + "\n")
        sys.exit()
    if value is not None:
        memoryStorage[key] = value
    else:
        try:
            return memoryStorage[key]
        except:
            sys.stderr.write("ERREUR : Nom de variable inconnue : " + key)
            sys.exit()


def noLoop():
    global loopLock
    loopLock = True


def cleanScreen():
    global screenCleen
    screenCleen = True


def getMouseLeftClick():
    if mouseclickL:
        return mouseclickleft


def getMouseRightClick():
    if mouseclickR:
        return mouseclickright


def getkeyPress():
    return keyPress


def getKeyPressList(value):
    if keyPressList is not None:
        if len(keyPressList) > value:
            return keyPressList[value] == 1
    return False


def getkeyPressValue():
    return keyPressValue


def getkeyRelease():
    return keyReleaseValue


def setup():
    pygame.init()
    global WINDOW_SIZE
    WINDOW_SIZE
    if (setupfunction is not None):
        setupfunction()

    global screen
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Window")


def run():
    if (runfuntion is not None):
        runfuntion()


def main(setupf, runf):
    print(inspect.stack()[1].function)
    global runfuntion
    runfuntion = runf
    global setupfunction
    setupfunction = setupf
    global keyPressList, screenCleen, mouseclickleft, mouseclickL, mouseclickright, mouseclickR, keyPress, keyPressValue, keyReleaseValue, screen

    setup()

    clock = pygame.time.Clock()

    done = False
    print("Run START-----------")
    while not done:

        if not loopLock:
            if screenCleen:
                screenCleen = False
                screen.fill(0)
            run()

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            elif event.type == pygame.KEYDOWN:
                keyPress = True
                keyPressValue = event.key

            elif event.type == pygame.KEYUP:
                keyPressValue = None

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    mouseclickL = True
                    mouseclickleft = event.pos
                if event.button == 3:
                    mouseclickR = True
                    mouseclickright = event.pos


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseclickL = False
                    mouseclickleft = None
                if event.button == 3:
                    mouseclickR = False
                    mouseclickright = None

            elif event.type == pygame.MOUSEMOTION:
                if mouseclickL:
                    mouseclickleft = event.pos
                if mouseclickR:
                    mouseclickright = event.pos

            if hasattr(event, 'key'):
                keyPressList = pygame.key.get_pressed()
                if keyPressValue:
                    keyReleaseValue = event.key
                else:
                    keyReleaseValue = None

        clock.tick(fps)

        # print(clock.get_time())
        # Go ahead and update the screen with what we 've drawn.
        pygame.display.flip()