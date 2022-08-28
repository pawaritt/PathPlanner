from cmath import inf
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
    
    def y_transform(self, dis):
        self.bias += dis

    def padding(self, pad):
        self.y_transform(pad / abs(math.sin(math.atan(-self.x_bar/self.y_bar))))

    def calculate_dist(self):
        x = abs(self.pos0.x - self.pos1.x)
        y = abs(self.pos0.y - self.pos1.y)
        dist_px = abs(math.hypot(x, y))
        self.dist = dist_px
        return dist_px

class PathPlanner:
    def __init__(self, points, object_size:int=100) -> None:
        self.points = [BasePoint(point) for point in points]
        print([(point.x, point.y) for point in self.points])
        self.sort_points()
        self.lines = [Line(self.points[0], self.points[3]), Line(self.points[1], self.points[2]), Line(self.points[0], self.points[1]), Line(self.points[2], self.points[3])]
        padding = round(object_size / 4)
        self.combo = sum_string([str(point.index) for point in self.sorted_points])
        print(self.combo)
        self.min_combination = quadrangle_com.MINIMUMLINE_SPLIT_POINT[self.combo]
        self.max_combination = quadrangle_com.MAXIMUM_SPLIT_POINT[self.combo]
        self.base_line = self.lines[0]
        angle = math.atan(self.base_line.y_bar / self.base_line.x_bar)
        self.padding = 25
        # self.x_padding = abs(self.padding * math.cos(angle))
        # self.y_padding = abs(self.padding * math.sin(angle))
        self.seed_space = 30
        self.split_dist = abs(40 / math.cos(math.radians(math.degrees(angle) + 90)))
        self.path = []
        self.z = 0
        self.p = 1
        self.y_seed_space = abs(self.seed_space * math.sin(angle))
        # test_line = Line(Point((0, 0)), Point((self.x_padding, self.y_padding)))

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
        print([(point.x, point.y) for point in points])
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
        xt = self.y_seed_space * -1
        points = list()
        if ((self.z - 1) > 0) and (self.p == -1):
            points.append({
                'pos': (min_p.x, min_p.y),
                })
            x1 = min_p.y
            while x1 - (xt * 1.5) < max_p.y:
                x1 -= xt
                points.append({
                    'pos': (cur_line.calculate_x(x1), x1)
                })
            points.append({
                'pos': (max_p.x, max_p.y),
                })
            self.p *= -1 

        elif ((self.z - 1) > 0) and (self.p == 1):
            points.append({
                'pos': (max_p.x, max_p.y),
                })
            x1 = max_p.y
            while x1 + (xt * 1.5 ) > min_p.y:
                x1 += xt
                points.append({
                    'pos': (cur_line.calculate_x(x1), x1)
                })
                # break
            points.append({
                'pos': (min_p.x, min_p.y),
                })
            self.p *= -1 
        else:
            points.append({
                'pos': (min_p.x, min_p.y),
                })
            x1 = min_p.y
            while x1 - (xt * 1.5) < max_p.y:
                x1 -= xt
                points.append({
                    'pos': (cur_line.calculate_x(x1), x1)
                })
            points.append({
                'pos': (max_p.x, max_p.y),
                })
        self.path.append(points)
                
    def calculate_path(self):
        min_x, max_x = self.sorted_points[0], self.sorted_points[3]
        i, min_index, max_index = 1, 0, 0
        min_p = min_x
        max_p = min_x
        x_pos = min_x.x
        x_dif = self.padding
        current_min_combination = self.min_combination[min_index]
        current_max_combination = self.max_combination[max_index]
        self.lines[current_min_combination['line'] - 1].padding(self.padding)
        self.lines[current_max_combination['line'] - 1].padding(-self.padding)
        if self.lines[1].slope < 0:
            self.lines[1].padding(-self.padding)
        else: 
            self.lines[1].padding(self.padding)
        min_lim_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(self.lines[1])
        max_lim_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(self.lines[1])
        while True:
            if (not (self.lines[current_min_combination['line'] - 1] == self.base_line)):
                min_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(self.base_line, x_dif)
            else:
                min_index += 1
                current_min_combination = self.min_combination[min_index]
                self.lines[current_min_combination['line'] - 1].padding(self.padding)
                min_lim_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(self.lines[1])
                continue

            max_lim_p = self.get_point_by_index(current_max_combination['point'])
            if not (self.lines[current_max_combination['line'] - 1] == self.base_line):
                max_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(self.base_line, x_dif)
            else:
                max_index += 1
                current_max_combination = self.max_combination[max_index]
                self.lines[current_max_combination['line'] - 1].padding(-self.padding)
                max_lim_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(self.lines[1])
                continue
            if (max_p.x > max_lim_p.x) or (min_p.x > min_lim_p.x):
                # break
                option = 0
                if self.combo == '0312' and self.base_line.slope < self.lines[1].slope:
                    option = 2
                elif self.combo == '0312':
                    option = 1
                elif self.combo == '3021' and self.base_line.slope < self.lines[1].slope:
                    option = 2
                elif self.combo == '3021':
                    option = 1
                elif self.combo == '3012':
                    option = 1
                elif self.combo == '0321':
                    option = 2
                if option == 1:
                    print('OPTION 1')
                    cur_line = Line(min_p, max_p)
                    cur_line.calculate_dist()
                    d = cur_line.dist + 10
                    new_d = cur_line.dist
                    while (new_d > 100):
                        d = new_d + 40
                        min_p = self.lines[current_max_combination['line'] - 1].get_intersection_point(cur_line)
                        # min_p.y -= self.y_padding
                        # min_p.x -= self.x_padding
                        max_p = cur_line.get_intersection_point(self.lines[1])
                        # max_p.y += self.y_padding
                        # max_p.x += self.x_padding
                        cur_line.transform(self.split_dist)
                        new_d = get_dist_btw_pos(min_p, max_p)
                        if (d < new_d):
                            break
                        self.add_path(max_p, min_p)
                        self.z += 1
                        x_dif += self.split_dist
                        if self.z > 100:
                            break
                elif option == 2:
                    print('OPTION 2')
                    cur_line = Line(min_p, max_p)
                    cur_line.calculate_dist()
                    d = cur_line.dist + 10
                    new_d = cur_line.dist
                    while (new_d > 100):
                        d = new_d + 40
                        min_p = cur_line.get_intersection_point(self.lines[1])
                        # min_p.y -= self.y_padding
                        # min_p.x -= self.x_padding
                        max_p = self.lines[current_min_combination['line'] - 1].get_intersection_point(cur_line)
                        # max_p.y += self.y_padding
                        # max_p.x += self.x_padding
                        cur_line.transform(self.split_dist)
                        new_d = get_dist_btw_pos(min_p, max_p)
                        if (d < new_d):
                            break
                        self.add_path(max_p, min_p)
                        self.z += 1
                        x_dif += self.split_dist
                        if self.z > 100:
                            break
                break
            x_dif += self.split_dist
            self.z += 1
            self.add_path(min_p, max_p)
            cur_line = Line(min_p, max_p)
        return self.path
