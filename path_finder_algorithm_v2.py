from math import comb
from function import *
import quadrangle_com

# ------------ inputs ----------^^^^^^^^

class BasePoint:
    def __init__(self, pos, index=None) -> None:
        self.x, self.y = pos[0], pos[1]
        self.index = index

class Point:
    def __init__(self, pos) -> None:
        self.x, self.y = pos[0], pos[1]

class Line:
    def __init__(self, pos0, pos1) -> None:
        self.x_bar = pos0.x - pos1.x
        self.y_bar = pos0.y - pos1.y
        self.pos0 = pos0
        self.pos1 = pos1
        self.slope = self.y_bar / (self.x_bar + 1.752e-13)
        self.bias = pos0.y - (self.slope * pos0.x)

    def calculate_y(self, x):
        return (self.slope * x) + self.bias
    
    def calculate_x(self, y):
        return (y - self.bias) / self.slope
    def get_intersection_point(self, line, l1_x_transformation = 0, l2_x_transformation=0):
        x_pos = ((line.bias + (line.slope * l1_x_transformation * -1)) - (self.bias + (self.slope * l2_x_transformation * -1))) / (self.slope - line.slope)
        return Point((x_pos, self.calculate_y(x_pos)))
    
    def dis_to_intersection_point(self, p1, p2, padding=0):
        dis = math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
        dis -= padding
        cal_dis = abs(self.y_bar * (dis / math.sqrt(self.x_bar**2 + self.y_bar**2)))
        return cal_dis
    
    def transform(self, dis):
        self.bias = self.bias + (self.slope * dis * -1)

class PathPlanner:
    def __init__(self, points, object_size:int=15) -> None:
        self.points = [BasePoint(point) for point in points]
        self.sort_points()
        print([(point.x, point.y) for point in self.sorted_points])
        self.lines = [Line(self.points[0], self.points[3]), Line(self.points[1], self.points[2]), Line(self.points[0], self.points[1]), Line(self.points[2], self.points[3])]
        padding = round(object_size / 4)
        combo = sum_string([str(point.index) for point in self.sorted_points])
        print(combo)
        self.min_combination = quadrangle_com.MINIMUMLINE_SPLIT_POINT[combo]
        self.max_combination = quadrangle_com.MAXIMUM_SPLIT_POINT[combo]
        self.base_line = self.lines[0]
        self.x_split_dist = round(object_size / 3)
        self.x_padding = abs(padding * (self.base_line.x_bar / math.sqrt(self.base_line.x_bar**2 + self.base_line.y_bar**2)))
        self.y_padding = abs(padding * (self.base_line.y_bar / math.sqrt(self.base_line.x_bar**2 + self.base_line.y_bar**2)))
        self.seed_space = 30
        self.path = []
        self.z = 1
        self.p = 1
        self.x_seed_space = abs(self.seed_space * (self.base_line.x_bar / math.sqrt(self.base_line.x_bar**2 + self.base_line.y_bar**2)))
        self.y_seed_space = abs(self.seed_space * (self.base_line.y_bar / math.sqrt(self.base_line.x_bar**2 + self.base_line.y_bar**2)))

    def sort_points(self):
        n = len(self.points)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1):
                if self.points[j].x > self.points[j + 1].x:
                    self.points[j], self.points[j + 1] = self.points[j + 1], self.points[j]
                    already_sorted = False
            if already_sorted:
                break
        self.sorted_points = self.points.copy()
        points = self.points
        if points[0].y < points[1].y:
            point_1 = points[0]
            point_4 = points[1]
        else:
            point_4 = points[0]
            point_1 = points[1]
        if points[2].y < points[3].y:
            point_2 = points[2]
            point_3 = points[3]
        else:
            point_3 = points[2]
            point_2 = points[3]
        point_1.index = 0
        point_2.index = 1
        point_3.index = 2
        point_4.index = 3
        self.points = (point_1, point_2, point_3, point_4)

    def get_point_by_index(self, index):
        for point in self.points:
            if point.index == index:
                return point
    
    def add_path(self, min_p, max_p):
        # print(self.z)
        cur_line = Line(min_p, max_p)
        if cur_line.slope < 0:
            xt = self.y_seed_space * -1
        if ((self.z - 1) > 0) and (self.p == -1):
            self.path.append({
                'pos': (min_p.x, min_p.y),
                })
            x1 = min_p.y
            while x1 - (xt * 1.5) < max_p.y:
                x1 -= xt
                self.path.append({
                    'pos': (cur_line.calculate_x(x1), x1)
                })
            self.path.append({
                'pos': (max_p.x, max_p.y),
                })
            self.p *= -1 

        elif ((self.z - 1) > 0) and (self.p == 1):
            self.path.append({
                'pos': (max_p.x, max_p.y),
                })
            x1 = max_p.y
            while x1 + (xt * 1.5 ) > min_p.y:
                x1 += xt
                self.path.append({
                    'pos': (cur_line.calculate_x(x1), x1)
                })
                # break
            self.path.append({
                'pos': (min_p.x, min_p.y),
                })
            self.p *= -1 
        else:
            self.path.append({
                'pos': (min_p.x, min_p.y),
                })
            x1 = min_p.y
            while x1 - (xt * 1.5) < max_p.y:
                x1 -= xt
                self.path.append({
                    'pos': (cur_line.calculate_x(x1), x1)
                })
            self.path.append({
                'pos': (max_p.x, max_p.y),
                })
                
    def calculate_path(self):
        min_x, max_x = self.sorted_points[0], self.sorted_points[3]
        i, min_index, max_index = 1, 0, 0
        min_p = min_x
        max_p = min_x
        x_pos = min_x.x
        while True:
            x_dif = self.x_split_dist * self.z
            x_pos += self.x_split_dist
            
            current_min_combination = self.min_combination[min_index]
            min_lim_p = self.get_point_by_index(current_min_combination['point'])
            if (not (self.lines[current_min_combination['line'] - 1] == self.base_line)) and (min_p.x < min_lim_p.x):
                min_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(self.base_line, x_dif)
                min_p.y += self.y_padding
            else:
                min_index += 1
                continue

            current_max_combination = self.max_combination[max_index]
            max_lim_p = self.get_point_by_index(current_max_combination['point'])
            if not (self.lines[current_max_combination['line'] - 1] == self.base_line) and (max_p.x < max_lim_p.x):
                max_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(self.base_line, x_dif)
                max_p.y -= self.y_padding
            else:
                max_index += 1
                continue
            if (max_p.x > max_lim_p.x) or (min_p.x > min_lim_p.x):
                self.path.pop()
                if self.base_line.slope > 0:
                    cur_line = Line(min_p, max_p)
                    max_last_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(self.base_line, x_dif - self.x_split_dist)
                    max_last_p.y += self.y_padding
                    self.path.extend([{
                                'pos': (min_last_p.x, min_last_p.y),
                            }])
                    while (get_dist_btw_pos(min_p, max_p) > 20) and (min_p.x < max_x.x):
                        x_dif = self.x_split_dist * self.z
                        max_p = cur_line.get_intersection_point(self.lines[1], -self.x_split_dist)
                        min_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(self.base_line, x_dif)
                        min_p.y -= self.y_padding
                        cur_line.transform(self.x_split_dist)
                        self.add_path(min_p, max_p)
                        self.z += 1
                        if self.z > 10000:
                            break
                elif self.base_line.slope < 0:
                    cur_line = Line(min_p, max_p)
                    min_last_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(self.base_line, x_dif - self.x_split_dist)
                    min_last_p.y -= self.y_padding
                    self.path.extend([{
                                'pos': (min_last_p.x, min_last_p.y),
                            }])
                    while (get_dist_btw_pos(min_p, max_p) > 50) and (max_p.x < max_x.x):
                        x_dif = self.x_split_dist * self.z
                        max_p = cur_line.get_intersection_point(self.lines[1], -self.x_split_dist)
                        min_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(self.base_line, x_dif)
                        min_p.y += self.y_padding
                        cur_line.transform(self.x_split_dist)
                        self.add_path(min_p, max_p)
                        self.z += 1
                        if self.z > 10000:
                            break
                break
            self.add_path(min_p, max_p)
            cur_line = Line(min_p, max_p)
            self.z += 1
        return self.path
