import pygame, random
from function import get_dist_btw_pos, get_angle_btw_line
from path_finder_algorithm_v2 import PathPlanner
from car import Car
import time
import os
import math
pygame.init()
# print(pygame.version)
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


def get_multiple_input(amount=10):
    screen = pygame.display.set_mode()
    input_point_sets = list()
    for x in range(amount):
        input_points = list()
        index = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    input_points.append(pos)
                    index += 1
            for i in range(len(input_points)):
                if i > 0:
                    pygame.draw.line(screen, (255, 0, 255), input_points[i - 1], input_points[i], 4)
                if i == 3:
                    pygame.draw.line(screen, (255, 0, 255), input_points[i], input_points[0], 4)
                pygame.draw.circle(screen, (0, 255, 0), input_points[i], radius=10, width=6)
            pygame.display.flip()
            if index == 4:
                break
        input_point_sets.append(input_points)
        pygame.display.flip()
    print(input_point_sets)
    return input_point_sets
        

class Simulation(object):
    def __init__(self, input_points=None):
        self.screen = pygame.display.set_mode()
        self.clock = pygame.time.Clock()
        self.player = Car(0, 0)
        if not input_points:
            self.input_points = []
            self.get_points()
        else:
            self.input_points = input_points
        planner = PathPlanner(self.input_points)
        self.lines = planner.calculate_path()
        # try: 
        #     self.moves = planner.calculate_path()
        # except:
        #     self.moves = []
        # print([move['pos'] for move in self.moves])
        pygame.display.set_caption("ANONYMOUS CAR ALGO TEST 1")

    def draw_points(self):
        for line in self.lines:
            for point in line:
                pygame.draw.circle(self.screen, (0, 255, 0), point['pos'], radius=4, width=2)

    def display(self, stop=False):
        self.draw_points()
        self.draw_lines()
        self.draw_path()
        pygame.display.update()
        x = 0
        if stop:
            i = 0
        else:
            i = 1
        while True:
            x += 1
            self.clock.tick(60)  
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = 0 
            if event.type == pygame.MOUSEBUTTONDOWN:
                i *= -1
                print(i)
            if x == 100 and i == 1:
                break

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
            for line in self.lines:
                for point in line:
                    if last_point:
                        pygame.draw.line(self.screen, (0, 0, 255), last_point, point['pos'], 3)
                    last_point = point['pos']
                    pygame.display.update()
                    time.sleep(delay)
        else:
            for line in self.lines:
                for point in line:
                    if last_point:
                        pygame.draw.line(self.screen, (0, 0, 255), last_point, point['pos'], 3)
                    last_point = point['pos']

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
    for points in get_multiple_input(7):
        s = Simulation(points)
        s.display(stop=False)
    # test_points = [[(74, 78), (1349, 49), (839, 635), (138, 743)], [(152, 118), (573, 598), (1423, 624), (1398, 120)], [(335, 81), (1245, 83), (1226, 846), (281, 809)], [(540, 157), (940, 167), (1332, 468), (273, 500)], [(232, 188), (538, 543), (1044, 748), (1317, 313)], [(579, 365), (728, 127), (1191, 123), (690, 781)], [(690, 418), (1343, 412), (1332, 648), (1006, 641)]]
    # for points in test_points:
    #     s = Simulation(points)
    #     s.display(stop=False)
    # test_point = [(579, 365), (728, 127), (1191, 123), (690, 781)]
    # s = Simulation(test_point)
    # s.display(True)
    # s = Simulation()
    # s.display(True)
    # s.run()