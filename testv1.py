import cv2
import pygame
import numpy as np
from function import *
import time

from path_finder_algorithm import PathPlanner
MAP_SIZE_COEFF = 5.14

input_points = [(138, 63), (435, 67), (492, 315), (155, 342)]


pygame.init()
pygame.display.set_caption("ANONYMOUS CAR - PATH PLANNER")

surface = pygame.display.set_mode([640, 480])


WHITE = (255, 255, 255)
 
class Car(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
 
    def __init__(self, color, width, height, speed):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.image.load("car.png").convert_alpha()
        #Initialise attributes of the car.
        self.width=width
        self.height=height
        self.color = color
        self.speed = speed
 
        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
 
        # Instead we could load a proper picture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
 
    def moveRight(self, pixels):
        self.rect.x += pixels
 
    def moveLeft(self, pixels):
        self.rect.x -= pixels
 
    def moveForward(self, speed):
        self.rect.y += self.speed * speed / 20
 
    def moveBackward(self, speed):
        self.rect.y -= self.speed * speed / 20
 
    def changeSpeed(self, speed):
        self.speed = speed
 
    def repaint(self, color):
        self.color = color
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])

def draw_lines(paths):
    for i in range(len(paths)):
        if i > 0:
            pygame.draw.line(surface, (255, 0, 255), paths[i - 1], paths[i], 4)
        if i == 3:
            pygame.draw.line(surface, (255, 0, 255), paths[i], paths[0], 4)
        pygame.draw.circle(surface, (0, 255, 0), paths[i], radius=10, width=6)
        pygame.display.update()

def draw_path(paths, delay:int=None):
    if delay:
        for path in paths:
            pygame.draw.line(surface, (0, 0, 255), path[1], path[0], 3)
            pygame.draw.circle(surface, (0, 255, 0), path[1], radius=4, width=4)
            pygame.display.update()
            time.sleep(delay)
    else:
        for path in paths:
            pygame.draw.line(surface, (0, 0, 255), path[1], path[0], 3)

print('run')
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

quad = PathPlanner(input_points, 25)
lines = quad.calculate_path()
draw_path(lines, 1)
displaying = True
while displaying:
    draw_lines(input_points)
    draw_path(lines)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



# Save to JSON file.
# print(waypoints)
pygame.quit()
