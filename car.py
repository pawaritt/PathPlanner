import pygame
from pygame.math import Vector2
import math
import os
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Car:
    def __init__(self, x, y) -> None:
        self.image_orig = pygame.image.load("assets/146513-car-top-view-png-image-high-quality.png").convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (100, 80))
        self.image = self.image_orig.copy()  
        self.image.set_colorkey((0, 0, 0))  
        self.rect = self.image.get_rect()  
        self.rect.center = [x , y]
        self.rot_speed = 10
        self.rot = 0
        self.angle = 0

    def move(self, x, y):
        old_center = list(self.rect.center)
        self.rect.center = (x, y)

    def forward(self, distance):
        old_center = list(self.rect.center)
        angle = (self.angle + 90) % 360 
        x = math.cos(math.radians(angle)) * distance
        y = math.sin(math.radians(angle)) * distance 
        # print(x)
        # print(y)
        # print(old_center[0] + x, old_center[1] - y)
        self.rect.center = (float(old_center[0] + x), old_center[1] - y)
        # print(self.rect.center)
        # print(self.rect)

    def draw(self, surf):
        surf.blit(self.image, self.rect)
    
    def rotate(self, angle):
        self.angle = abs(360 - angle) % 360
        old_center = self.rect.center    
        self.image = pygame.transform.rotate(self.image_orig , self.angle)  
        self.rect = self.image.get_rect()  
        self.rect.center = old_center  
