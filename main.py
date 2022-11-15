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
        self.main_thrust = self.font.render("Thrust: " + str(int(player.main_thrust)), True, WHITE)

    def draw(self, surface):
        surface.blit(self.speed, (self.location_x, self.location_y))
        surface.blit(self.main_thrust, (self.location_x, self.location_y + 25))
 
 
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__() 

        # Define the sprite image and size
        self.suface_width, self.surface_height = pygame.display.get_surface().get_size()
        self.image = pygame.image.load("assets/img/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 600)

        # Set Maximum values for different speeds
        self.MAX_AFTERBURNER = 200
        self.MAX_SPEED = 120
        self.MAX_THRUST = 5
        
        # Set initial values
        self.speed = 0          # speed relative to the universe
        self.v_thrust = 0       # vertical speed relative to the screen
        self.h_thrust = 0       # horizontal speed relative to the screen
        self.main_engines = False   # ship starts stopped
        
        # Accelaration values
        self.main_thrust = 0    # How fast the ship accelerates relative to the universe
        self.thrusters = 0.4    # How fast the ship accelerates relative to the screen.
        self.afterburners = 2   # How fast the afterburner accelerates the ship.
        self.drag = 0.97        # How fast the drag will decelarate movement ( 1 = no drag )

        # Load sound effects
        self.boing_sound = pygame.mixer.Sound("assets/sounds/boing.wav")
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.image = pygame.image.load("assets/img/player.png")

        # Move up
        if self.rect.top > (100):
            if pressed_keys[K_UP] and self.v_thrust > -self.MAX_THRUST:
                self.v_thrust -= self.thrusters
        elif self.rect.top <= (100) and self.v_thrust < 0:
            self.v_thrust = 0

        # Move down
        if self.rect.bottom < (self.surface_height-100):
            if pressed_keys[K_DOWN] and self.v_thrust < self.MAX_THRUST:
                self.v_thrust += self.thrusters
        elif self.rect.bottom >= (self.surface_height-100) and self.v_thrust > 0:
            self.v_thrust = 0

        # Move left
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.image = pygame.image.load("assets/img/player_left.png")
                if self.h_thrust > -self.MAX_THRUST:
                    self.h_thrust -= self.thrusters
        elif self.rect.left <= 0 and self.h_thrust < 0:
            self.h_thrust = -self.h_thrust  # bounce if player hits screen edge
            pygame.mixer.Sound.play(self.boing_sound)

        # Move right
        if self.rect.right < self.suface_width:        
            if pressed_keys[K_RIGHT]:
                self.image = pygame.image.load("assets/img/player_right.png")
                if self.h_thrust < self.MAX_THRUST:
                    self.h_thrust += self.thrusters
        elif self.rect.right >= self.suface_width and self.h_thrust > 0:
            self.h_thrust = -self.h_thrust  # bounce if player hits screen edge
            pygame.mixer.Sound.play(self.boing_sound)

        # Engage Engine
        if pressed_keys[K_w]:
            self.main_engines = True

        # Disengage Engine
        if pressed_keys[K_s]:
            self.main_engines = False
            self.main_thrust = 0

        self.rect.move_ip(self.h_thrust, self.v_thrust)

        # Apply drag coefficient to all speeds relative to the screen.
        if self.h_thrust != 0:
            self.h_thrust *= self.drag
        if self.v_thrust != 0:
            self.v_thrust *= self.drag
        if self.speed != 0:
            self.speed *= self.drag

        # Ship keeps accelerating until it reaches MAX_SPEED
        if self.main_engines is True:
            if self.main_thrust < self.MAX_THRUST:
                self.main_thrust += self.thrusters/10
            self.speed += self.main_thrust
            if self.speed > self.MAX_SPEED:
                self.speed = self.MAX_SPEED

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
        self.background.update(self.P1.speed)
        self.texture.update(self.P1.speed*.9)
        self.star_field_1.update(self.P1.speed*0.01)
        self.star_field_2.update(self.P1.speed*0.05)
        self.hud.update(self.P1)


scene = Scene()

# Game Loop
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    scene.update()
    scene.drawScene()     
    FramePerSec.tick(FPS)