#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Pre-define some colours
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Background
background = pygame.image.load("assets/img/background.png")
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
      def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/img/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 600)
        self.speed = 0
        self.MAX_SPEED = 50
        self.thrusters = 0.5
        self.drag = 0.1
        self.v_thrust = 0
        self.h_thrust = 0
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.image = pygame.image.load("assets/img/player.png")

        # Move up
        if self.rect.top > (100):
            if pressed_keys[K_UP]:
                self.v_thrust -= self.thrusters
        # Stop upward thrust if at top
        elif self.rect.top <= (100) and self.v_thrust < 0:
            self.v_thrust = 0

        # Move down
        if self.rect.bottom < (SCREEN_HEIGHT-100):
            if pressed_keys[K_DOWN]:
                self.v_thrust += self.thrusters
        # Stop downward thrust if at bottom
        elif self.rect.bottom >= (SCREEN_HEIGHT-100) and self.v_thrust > 0:
            self.v_thrust = 0

        # Move left
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.image = pygame.image.load("assets/img/player_left.png")
                self.h_thrust -= self.thrusters
        # Stop left movement if at edge of screen
        elif self.rect.left <= 0 and self.h_thrust < 0:
            self.h_thrust = 0

        # Move right
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.image = pygame.image.load("assets/img/player_right.png")
                self.h_thrust += self.thrusters
        # Stop right movement if at edge of screen
        elif self.rect.right >= SCREEN_WIDTH and self.h_thrust > 0:
            self.h_thrust = 0

        self.rect.move_ip(self.h_thrust, self.v_thrust)

        if self.h_thrust > 0:
            self.h_thrust -= self.drag
        if self.h_thrust < 0:
            self.h_thrust += self.drag

        if self.v_thrust > 0:
            self.v_thrust -= self.drag
        if self.v_thrust < 0:
            self.v_thrust += self.drag

        if self.speed < self.MAX_SPEED:
            if pressed_keys[K_w]:
                self.speed += 0.1

        if self.speed > 0:
            if pressed_keys[K_s]:
                self.speed -= 0.1

 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
 
         
P1 = Player()
#E1 = Enemy()

def redrawWindow():
    DISPLAYSURF.blit(background, (0,0))
    P1.draw(DISPLAYSURF)
    #E1.draw(DISPLAYSURF)
    pygame.display.update()

# Game Loop
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    #E1.move()

    redrawWindow()     
    FramePerSec.tick(FPS)