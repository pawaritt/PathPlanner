import math
import numpy as np
MAP_SIZE_COEFF = 5.14
points = [(478, 264.08771929824616), (478, 306.1216617210682), (488, 307.59649122807105)]
def get_dist_btw_pos(pos0, pos1):
    """
    Get distance between 2 mouse position.
    """
    x = abs(pos0.x - pos1.x)
    y = abs(pos0.y - pos1.y)
    dist_px = math.hypot(x, y)
    return dist_px

def get_angle_btw_line(pos0, pos1, posref):
    """
    Get angle between two lines respective to 'posref'
    NOTE: using dot product calculation.
    """
    # print(pos0, pos1, posref)
    ax = posref.x - pos0.x
    ay = posref.y - pos0.y
    bx = posref.x - pos1.x
    by = posref.y - pos1.y
    # print(pos0.x, pos0.y)
    # print(posref.x, posref.y)
    # print(pos1.x, pos1.y)
    # print(ax, ay)
    # print(bx, by)
    # Get dot product of pos0 and pos1.
    _dot = (ax * bx) + (ay * by)
    # Get magnitude of pos0 and pos1.
    
    _magA = math.sqrt(ax**2 + ay**2)
    _magB = math.sqrt(bx**2 + by**2)
    _rad = math.acos(_dot / (_magA * _magB))
    # Angle in degrees.
    angle = (_rad * 180) / math.pi
    # print(angle)
    return angle

# def get_angle_btw_pos(pos0, pos1, pos2):
#     print(pos1)
#     x1_pos_array = np.array([pos0[0], pos1[0], pos2[0]])
#     x2_pos_array = np.array([pos1[0], pos2[0], pos0[0]])
#     y1_pos_array = np.array([pos0[1], pos1[1], pos2[1]])
#     y2_pos_array = np.array([pos1[1], pos2[1], pos0[1]])

#     a, c, b = np.sqrt(np.sum([np.subtract(x1_pos_array, x2_pos_array) **2, np.subtract(y1_pos_array, y2_pos_array)**2], axis=0))
    
#     rad = math.acos((c**2 - (a**2 + b**2)) / (-2*a*b))
    # print(rad)

def sum_string(lst):
    s = ''
    for element in lst:
        s += element
    return s

# angle = get_angle_btw_line(*points)
# print(angle)
# angle2 = get_angle_btw_pos(*points)

