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
pygame.font.init()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40, screen_width-40),0) 
 
    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 

class HUD():
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 20)
        self.location_x = 450
        self.location_y = 10

    def update(self, player):
        self.speed = self.font.render("Speed: " + str(int(player.speed)), True, WHITE)

    def draw(self, surface):
        surface.blit(self.speed, (self.location_x, self.location_y))
 
 
class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__() 

        # Define the sprite image and size
        self.suface_width, self.surface_height = pygame.display.get_surface().get_size()
        self.image = pygame.image.load("assets/img/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 600)

        # Set Maximum values for different speeds
        self.max_thrust = 50
        self.mass = 10
        
        # Set initial values
        self.speed = 0          # speed relative to the universe
        self.main_thrust = 200
        self.v_speed = 0       # vertical speed relative to the screen
        self.h_speed = 0       # horizontal speed relative to the screen
        self.main_engines = False   # ship starts stopped
        
        # Accelaration values
        self.thrusters = 4    # How fast the ship accelerates relative to the screen.
        self.drag = 0.015        # How fast the drag will decelarate movement ( 0 = no drag )

        # Load sound effects
        self.boing_sound = pygame.mixer.Sound("assets/sounds/boing.wav")
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.image = pygame.image.load("assets/img/player.png")

        # Maneuvering thrusters
        if self.main_engines is True:
            if pressed_keys[K_UP] and self.v_speed > -self.max_thrust:
                self.v_speed -= self.thrusters/self.mass
            if pressed_keys[K_DOWN] and self.v_speed < self.max_thrust:
                self.v_speed += self.thrusters/self.mass
            if pressed_keys[K_LEFT]:
                self.image = pygame.image.load("assets/img/player_left.png")
                if self.h_speed > -self.max_thrust:
                    self.h_speed -= self.thrusters/self.mass
            if pressed_keys[K_RIGHT]:
                self.image = pygame.image.load("assets/img/player_right.png")
                if self.h_speed < self.max_thrust:
                    self.h_speed += self.thrusters/self.mass

        # Bounding box for maneuveuring
        if self.rect.top <= (100) and self.v_speed < 0:
            self.v_speed = 0        
        if self.rect.bottom >= (self.surface_height-100) and self.v_speed > 0:
            self.v_speed = 0
        if self.rect.left <= 0 and self.h_speed < 0:
            self.h_speed = -self.h_speed  # bounce player off screen edge
            pygame.mixer.Sound.play(self.boing_sound)
        if self.rect.right >= self.suface_width and self.h_speed > 0:
            self.h_speed = -self.h_speed  # bounce player off screen edge
            pygame.mixer.Sound.play(self.boing_sound)

        self.rect.move_ip(self.h_speed, self.v_speed)

        # Main engines
        if pressed_keys[K_w]:
            self.main_engines = True
        if pressed_keys[K_s]:
            self.main_engines = False 

        # Ship keeps accelerating until it reaches MAX_SPEED
        if self.main_engines is True:
            self.speed += self.main_thrust/self.mass

        # Afterburners
        if pressed_keys[K_LSHIFT] and self.main_engines is True:
            self.speed += (self.main_thrust*3)/self.mass

        # Apply drag coefficient to all speeds relative to the screen.
        if self.h_speed != 0:
            self.h_speed *= (1 - self.drag)
        if self.v_speed != 0:
            self.v_speed *= (1 - self.drag)
        if self.speed != 0:
            self.speed -= (self.drag*(self.speed**2))/self.mass

    def draw(self, surface):
        surface.blit(self.image, self.rect)   


class ScrollingBackground:

    def __init__(self, img_path):
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
        self.screen_width = 600
        self.screen_height = 800
        self.display_surf = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.background = ScrollingBackground("assets/img/background.png")
        self.texture = ScrollingBackground("assets/img/background_texture.png")
        self.star_field_1 = ScrollingBackground("assets/img/star_field_1.png")
        self.star_field_2 = ScrollingBackground("assets/img/star_field_2.png")
        self.P1 = Player()
        self.hud = HUD()

    def drawScene(self):
        self.display_surf.fill(WHITE)
        self.background.draw(self.display_surf)
        self.texture.draw(self.display_surf)
        self.star_field_1.draw(self.display_surf)
        self.star_field_2.draw(self.display_surf)
        self.hud.draw(self.display_surf)
        self.P1.draw(self.display_surf)
        pygame.display.update()

    def update(self):
        self.P1.update()
        self.background.update(self.P1.speed*0.02)
        self.texture.update(self.P1.speed*0.09)
        self.star_field_1.update(self.P1.speed*0.01)
        self.star_field_2.update(self.P1.speed*0.05)
        self.hud.update(self.P1)

        self.drawScene()


scene = Scene()

# Game Loop
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    scene.update()  
    FramePerSec.tick(FPS)