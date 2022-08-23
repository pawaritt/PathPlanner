import pygame, random
from function import get_dist_btw_pos, get_angle_btw_line
from path_finder_algorithm_v2 import PathPlanner
from car import Car
import time
import os
import math
pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
        


class Simulation(object):
    def __init__(self):
        self.screen = pygame.display.set_mode()
        self.clock = pygame.time.Clock()
        self.player = Car(0, 0)
        # self.input_points = []
        self.input_points = [(782, 136), (1356, 228), (979, 507), (690, 425)]
        # self.get_points()
        print(self.input_points)
        planner = PathPlanner(self.input_points, 120)
        self.moves = planner.calculate_path()

        # try: 
        #     self.moves = planner.calculate_path()
        # except:
        #     self.moves = []
        # print([move['pos'] for move in self.moves])
        pygame.display.set_caption("ANONYMOUS CAR ALGO TEST 1")

    def draw_points(self):
        for move in self.moves:
            pygame.draw.circle(self.screen, (0, 255, 0), move['pos'], radius=4, width=2)

    def display(self):
        self.draw_points()
        self.draw_lines()
        # self.draw_path()
        pygame.display.update()
        while True:
            self.clock.tick(60)     
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = 0 

    def run(self):
        running = 1
        # print(self.moves)
        for i in range(len(self.moves)):
            self.clock.tick(60)     
            move = self.moves[i]
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = 0 
            if i < 1:
                self.player.move(move['pos'][0], move['pos'][1])
            else:
                move['angle'] = get_angle_btw_line((self.player.rect.center[0], self.player.rect.center[1] - 10), move['pos'], self.player.rect.center)
                self.get_to_point(move)
            self.refresh()

    def refresh(self):
        game_over_font = pygame.font.SysFont('Helvetica', 20)
        game_over = game_over_font.render("rad: %s"%self.player.angle, True, (0, 0, 0))
        self.screen.blit(game_over, (40, 40))
        self.player.draw(self.screen) 
        pygame.display.flip()

    def get_to_point(self,  move):
        self.player.rotate(move['angle'])
        self.refresh()
        pos = move['pos']
        distance = get_dist_btw_pos(self.player.rect.center, pos)
        while distance > 20:
            self.player.forward(6)
            distance = get_dist_btw_pos(self.player.rect.center, pos)
            self.screen.fill([255, 255, 255])
            self.draw_lines()
            self.draw_path()
            self.refresh()
            pygame.display.update()
            time.sleep(0.01)
        self.player.forward(distance)

    def draw_lines(self):
        for i in range(len(self.input_points)):
            if i > 0:
                pygame.draw.line(self.screen, (255, 0, 255), self.input_points[i - 1], self.input_points[i], 4)
            if i == 3:
                pygame.draw.line(self.screen, (255, 0, 255), self.input_points[i], self.input_points[0], 4)
            pygame.draw.circle(self.screen, (0, 255, 0), self.input_points[i], radius=10, width=6)

    def draw_path(self, delay:int=None):
        last_point = None
        if delay:
            for move in self.moves:
                if last_point:
                    pygame.draw.line(self.screen, (0, 0, 255), last_point, move['pos'], 3)
                last_point = move['pos']
                pygame.display.update()
                time.sleep(delay)
        else:
            for move in self.moves:
                if last_point:
                    pygame.draw.line(self.screen, (0, 0, 255), last_point, move['pos'], 3)
                last_point = move['pos']

    def get_points(self):
        index = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.input_points.append(pos)
                    index += 1
            self.draw_lines()
            pygame.display.flip()
            if index == 4:
                break

if __name__ == "__main__":
    s = Simulation()
    s.display()
    # s.run()