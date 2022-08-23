import cv2
import pygame
import pygame.camera
import numpy as np
from function import *
import time

from path_finder_algorithm import PathPlanner
MAP_SIZE_COEFF = 5.14

pygame.init()
pygame.display.set_caption("ANONYMOUS CAR - PATH PLANNER")

pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
cam.start()
width, height = cam.get_size()
print(width, height)
surface = pygame.display.set_mode([width, height])

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
            pygame.display.update()
            time.sleep(1)
    else:
        for path in paths:
            pygame.draw.line(surface, (0, 0, 255), path[1], path[0], 3)

def get_path():
    path_wp = []
    index = 0
    while True:
        img = cam.get_image()
        surface.blit(img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                path_wp.append(pos)
                index += 1
        draw_lines(path_wp)
        if index == 4:
            break
running = True
while running:
    path_wp = get_path()
    quad = PathPlanner(path_wp)
    lines = quad.calculate_path()
    img = cam.get_image()
    surface.blit(img, (0,0))
    draw_lines(path_wp)
    draw_path(lines, 100)
    displaying = True
    while displaying:
        img = cam.get_image()
        surface.blit(img, (0,0))
        draw_lines(path_wp)
        draw_path(lines)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('break')
                displaying = False
    

# Save to JSON file.
# print(waypoints)
cam.stop()
pygame.quit()
