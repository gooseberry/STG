#!/usr/bin/env python3

import pygame
from pygame.locals import *

pygame.init()


# Game Loop
while True:
    
    pygame.display.update()

    # quit game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit