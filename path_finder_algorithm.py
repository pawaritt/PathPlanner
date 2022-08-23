from math import comb
from function import *
import quadrangle_com

# ------------ inputs ----------^^^^^^^^

class Point:
    def __init__(self, index, pos) -> None:
        self.x, self.y = pos[0], pos[1]
        self.index = index

class Line:
    def __init__(self, pos0, pos1) -> None:
        x_bar = pos0.x - pos1.x
        y_bar = pos0.y - pos1.y
        self.pos0 = pos0
        self.pos1 = pos1
        self.slope = y_bar / (x_bar + 1.752e-13)
        self.bias = pos0.y - (self.slope * pos0.x)

    def calculate_y(self, x):
        return (self.slope * x) + self.bias

class PathPlanner:
    def __init__(self, points, object_size:int=15) -> None:
        self.points = [Point(index, point) for index, point in enumerate(points)]
        self.sorted_points = self.sort_points()
        self.lines = [Line(self.points[0], self.points[3]), Line(self.points[1], self.points[2]), Line(self.points[0], self.points[1]), Line(self.points[2], self.points[3])]
        self.x_total_dist = abs(self.sorted_points[0].x - self.sorted_points[3].x)
        self.x_split_dist = round(object_size / 1.5)
    

    def sort_points(self):
        # We set swapped to True so the loop looks runs at least once
        if self.points[0].x > self.points[3].x:
            self.points[3].sorted_index = 1 
            self.points[0].sorted_index = 2
            min_1 = self.points[3]
            min_2 = self.points[0]
        else:
            self.points[0].sorted_index = 1
            self.points[3].sorted_index = 2
            min_1 = self.points[0]
            min_2 = self.points[3]
        if self.points[1].x > self.points[2].x:
            self.points[2].sorted_index = 3
            self.points[1].sorted_index = 4
            min_3 = self.points[2]
            min_4 = self.points[1]
        else:
            self.points[1].sorted_index = 3
            self.points[2].sorted_index = 4
            min_3 = self.points[1]
            min_4 = self.points[2]
        return min_1, min_2, min_3, min_4

    def get_point_by_index(self, index):
        for point in self.points:
            if point.index == index:
                return point
    
    def calculate_path(self):
        path_angle, path_dist = [], []
        min_x, max_x = self.sorted_points[0], self.sorted_points[3]
        z, min_index, max_index, p = 1, 0, 0, 1
        combo = sum_string([str(point.index) for point in self.sorted_points])
        min_combination = quadrangle_com.MINIMUMLINE_SPLIT_POINT[combo]
        max_combination = quadrangle_com.MAXIMUM_SPLIT_POINT[combo]
        output = list()
        while True:
            x_pos = min_x.x + self.x_split_dist * z
            if x_pos > max_x.x:
                break
            current_min_combination = min_combination[min_index]
            if x_pos < self.get_point_by_index(current_min_combination['point']).x:
                y_min = self.lines[current_min_combination['line'] - 1].calculate_y(x_pos) + self.x_split_dist
            else:
                min_index += 1
                continue
            current_max_combination = max_combination[max_index]
            if x_pos < self.get_point_by_index(current_max_combination['point']).x:
                y_max = self.lines[current_max_combination['line'] - 1].calculate_y(x_pos) - self.x_split_dist
            else:
                max_index += 1
                continue
            if ((z - 1) > 0) and (p == -1):
                output.extend([[(last_x_pos, last_y_min), (x_pos, y_min)]])
                output.extend([[(x_pos, y_min), (x_pos, y_max)]])
                p *= -1 
            elif ((z - 1) > 0) and (p == 1):
                output.extend([[(last_x_pos, last_y_max), (x_pos, y_max)]])
                output.extend([[(x_pos, y_max), (x_pos, y_min)]])
                p *= -1 
            else:
                output.extend([[(x_pos, y_min), (x_pos, y_max)]])
            z += 1
            last_x_pos = x_pos
            last_y_min = y_min
            last_y_max = y_max

        return output
        # return [[(line.pos0.x, line.pos0.y), (line.pos1.x, line.calculate_y(line.pos1.x))] for line in self.lines]
        # if (self.points[0].x < self.points[3].x) and (self.points[0].x < self.points[1]):
        #     if (self.points[0] < x_pos < self.points[3]) and (self.points[0] < x_pos < self.points[1]):
        #         y_max = self.line1.calculate_y(x_pos)
        #         y_min = self.line3.calculate_y(x_pos)
        #     elif (self.points[0] < x_pos < self.points[3]) and (self.points[0] < x_pos < self.points[1]):
        #         y_max = self.line1.calculate_y(x_pos)
        #         y_min = self.line3.calculate_y(x_pos)
            


# quad = Quadrangle(input_points)
# quad.calculate_path()
