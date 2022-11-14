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
 
# Background

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
    def __init__(self, surface):
        super().__init__() 
        self.suface_width, self.surface_height = pygame.display.get_surface().get_size()
        self.image = pygame.image.load("assets/img/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 600)
        self.speed = 0
        self.MAX_SPEED = 50
        self.MAX_THRUST = 5
        self.thrusters = 0.4
        self.drag = 0.97
        self.v_thrust = 0
        self.h_thrust = 0
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.image = pygame.image.load("assets/img/player.png")

        # Move up
        if self.rect.top > (100):
            if pressed_keys[K_UP] and self.v_thrust > -self.MAX_THRUST:
                self.v_thrust -= self.thrusters
        # Stop upward thrust if at top
        elif self.rect.top <= (100) and self.v_thrust < 0:
            self.v_thrust = 0

        # Move down
        if self.rect.bottom < (self.surface_height-100):
            if pressed_keys[K_DOWN] and self.v_thrust < self.MAX_THRUST:
                self.v_thrust += self.thrusters
        # Stop downward thrust if at bottom
        elif self.rect.bottom >= (self.surface_height-100) and self.v_thrust > 0:
            self.v_thrust = 0

        # Move left
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.image = pygame.image.load("assets/img/player_left.png")
                if self.h_thrust > -self.MAX_THRUST:
                    self.h_thrust -= self.thrusters
        # Stop left movement if at edge of screen
        elif self.rect.left <= 0 and self.h_thrust < 0:
            self.h_thrust = 0

        # Move right
        if self.rect.right < self.suface_width:        
            if pressed_keys[K_RIGHT]:
                self.image = pygame.image.load("assets/img/player_right.png")
                if self.h_thrust < self.MAX_THRUST:
                    self.h_thrust += self.thrusters
        # Stop right movement if at edge of screen
        elif self.rect.right >= self.suface_width and self.h_thrust > 0:
            self.h_thrust = 0

        self.rect.move_ip(self.h_thrust, self.v_thrust)

        # Slow down movement
        if self.h_thrust != 0 :
            self.h_thrust *= self.drag
        if self.v_thrust != 0:
            self.v_thrust *= self.drag

        if self.speed < self.MAX_SPEED:
            self.speed += 0.1


 
    def draw(self, surface):
        surface.blit(self.image, self.rect)   

class ScrollingBackground:
    def __init__(self, surface, img_path):
        self.suface_width, self.surface_height = pygame.display.get_surface().get_size()
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img_ypos = - self.surface_height

    def draw(self, surface):
        surface.blit(self.img, (0, self.img_ypos))
        surface.blit(self.img, (0, self.img_ypos + self.surface_height))

    def update(self, speed):
        self.img_ypos += speed
        if self.img_ypos > 0:
            self.img_ypos = - self.surface_height


class Scene:
    def __init__(self):

        # Screen information
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 800
        self.DISPLAYSURF = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.background = ScrollingBackground(self.DISPLAYSURF, "assets/img/background.png")
        self.texture = ScrollingBackground(self.DISPLAYSURF, "assets/img/background_texture.png")
        self.P1 = Player(self.DISPLAYSURF)

    def drawScene(self):
        self.DISPLAYSURF.fill(WHITE)
        self.background.draw(self.DISPLAYSURF)
        self.texture.draw(self.DISPLAYSURF)
        self.P1.draw(self.DISPLAYSURF)
        pygame.display.update()

    def update(self):
        self.P1.update()
        self.background.update(self.P1.speed)
        self.texture.update(self.P1.speed*.9)
 
        

def redrawWindow():
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background, (0,0))
    DISPLAYSURF.blit(texture, (0,0))
    P1.draw(DISPLAYSURF)
    #E1.draw(DISPLAYSURF)
    pygame.display.update()

scene = Scene()

# Game Loop
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    scene.update()
    #E1.move()

    scene.drawScene()     
    FramePerSec.tick(FPS)