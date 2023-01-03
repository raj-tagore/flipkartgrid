import socket
import time
from threading import Thread
from multiprocessing import Process
import pandas as pd
import cv2
import numpy as np

all_centers = ac = [[614, 569], [572, 569], [530, 569], [488, 569], [445, 569], [404, 569], [361, 569], [320, 569],
    [277, 569], [235, 569], [193, 569], [151, 569], [109, 569], [67, 569], [614, 527], [572, 527], [530, 527],
    [488, 527], [445, 527], [404, 527], [361, 527], [320, 527], [277, 527], [235, 527], [193, 527], [151, 527],
    [109, 527], [67, 527], [614, 485], [572, 485], [445, 485], [404, 485], [276, 485], [235, 485], [109, 485],
    [66, 485], [613, 443], [572, 443], [509, 465], [445, 443], [403, 443], [340, 465], [277, 443], [235, 443],
    [173, 465], [109, 443], [67, 443], [26, 402], [614, 402], [572, 402], [530, 402], [488, 402], [445, 402],
    [404, 402], [361, 402], [320, 402], [277, 402], [235, 402], [193, 402], [151, 402], [109, 402], [67, 402],
    [614, 360], [572, 360], [530, 360], [488, 360], [445, 360], [404, 360], [361, 360], [320, 360], [277, 360],
    [235, 360], [193, 360], [151, 360], [109, 360], [67, 360], [614, 318], [572, 318], [445, 318], [404, 318],
    [276, 318], [235, 318], [109, 318], [67, 318], [613, 276], [572, 276], [509, 298], [445, 276], [404, 276],
    [340, 298], [277, 276], [235, 276], [173, 298], [109, 276], [67, 276], [614, 235], [572, 235], [530, 235],
    [488, 235], [445, 235], [404, 235], [361, 235], [320, 235], [277, 235], [235, 235], [193, 235], [151, 235],
    [109, 235], [67, 235], [26, 193], [614, 193], [572, 193], [530, 193], [488, 193], [445, 193], [404, 193],
    [361, 193], [320, 193], [277, 193], [235, 193], [193, 193], [151, 193], [109, 193], [67, 193], [614, 151],
    [572, 151], [445, 151], [404, 151], [277, 151], [235, 151], [109, 151], [67, 151], [614, 109], [572, 109],
    [509, 131], [445, 109], [404, 109], [340, 131], [277, 109], [235, 109], [173, 131], [109, 109], [67, 109],
    [614, 68], [572, 68], [530, 68], [488, 68], [445, 68], [404, 68], [361, 68], [320, 68], [277, 68], [235, 68],
    [193, 68], [151, 68], [109, 68], [67, 68], [614, 26], [572, 26], [530, 26], [488, 26], [445, 26], [404, 26],
    [361, 26], [320, 26], [277, 26], [235, 26], [193, 26], [151, 26], [109, 26], [67, 26]]
frame1_centers = all_centers[36:172]
frame2_centers = all_centers[0:110]
frame2_adjustment = 220

# node_map: dictionary with data of all nodes and their neighbors
# node_ids: array of all nodes bot can travel on
# city_ids: cities
# all_nodes: dict of: cell_id: [x-coord, y-coord]

all_nodes = {0: [614, 569], 1: [572, 569], 2: [530, 569], 3: [488, 569], 4: [445, 569], 5: [404, 569], 6: [361, 569],
    7: [320, 569], 8: [277, 569], 9: [235, 569], 10: [193, 569], 11: [151, 569], 12: [109, 569], 13: [67, 569],
    14: [614, 527], 15: [572, 527], 16: [530, 527], 17: [488, 527], 18: [445, 527], 19: [404, 527], 20: [361, 527],
    21: [320, 527], 22: [277, 527], 23: [235, 527], 24: [193, 527], 25: [151, 527], 26: [109, 527], 27: [67, 527],
    28: [614, 485], 29: [572, 485], 30: [445, 485], 31: [404, 485], 32: [276, 485], 33: [235, 485], 34: [109, 485],
    35: [66, 485], 36: [613, 443], 37: [572, 443], 38: [509, 465], 39: [445, 443], 40: [403, 443], 41: [340, 465],
    42: [277, 443], 43: [235, 443], 44: [173, 465], 45: [109, 443], 46: [67, 443], 47: [26, 402], 48: [614, 402],
    49: [572, 402], 50: [530, 402], 51: [488, 402], 52: [445, 402], 53: [404, 402], 54: [361, 402], 55: [320, 402],
    56: [277, 402], 57: [235, 402], 58: [193, 402], 59: [151, 402], 60: [109, 402], 61: [67, 402], 62: [614, 360],
    63: [572, 360], 64: [530, 360], 65: [488, 360], 66: [445, 360], 67: [404, 360], 68: [361, 360], 69: [320, 360],
    70: [277, 360], 71: [235, 360], 72: [193, 360], 73: [151, 360], 74: [109, 360], 75: [67, 360], 76: [614, 318],
    77: [572, 318], 78: [445, 318], 79: [404, 318], 80: [276, 318], 81: [235, 318], 82: [109, 318], 83: [67, 318],
    84: [613, 276], 85: [572, 276], 86: [509, 298], 87: [445, 276], 88: [404, 276], 89: [340, 298], 90: [277, 276],
    91: [235, 276], 92: [173, 298], 93: [109, 276], 94: [67, 276], 95: [614, 235], 96: [572, 235], 97: [530, 235],
    98: [488, 235], 99: [445, 235], 100: [404, 235], 101: [361, 235], 102: [320, 235], 103: [277, 235], 104: [235, 235],
    105: [193, 235], 106: [151, 235], 107: [109, 235], 108: [67, 235], 109: [26, 193], 110: [614, 193], 111: [572, 193],
    112: [530, 193], 113: [488, 193], 114: [445, 193], 115: [404, 193], 116: [361, 193], 117: [320, 193],
    118: [277, 193], 119: [235, 193], 120: [193, 193], 121: [151, 193], 122: [109, 193], 123: [67, 193],
    124: [614, 151], 125: [572, 151], 126: [445, 151], 127: [404, 151], 128: [277, 151], 129: [235, 151],
    130: [109, 151], 131: [67, 151], 132: [614, 109], 133: [572, 109], 134: [509, 131], 135: [445, 109],
    136: [404, 109], 137: [340, 131], 138: [277, 109], 139: [235, 109], 140: [173, 131], 141: [109, 109],
    142: [67, 109], 143: [614, 68], 144: [572, 68], 145: [530, 68], 146: [488, 68], 147: [445, 68], 148: [404, 68],
    149: [361, 68], 150: [320, 68], 151: [277, 68], 152: [235, 68], 153: [193, 68], 154: [151, 68], 155: [109, 68],
    156: [67, 68], 157: [614, 26], 158: [572, 26], 159: [530, 26], 160: [488, 26], 161: [445, 26], 162: [404, 26],
    163: [361, 26], 164: [320, 26], 165: [277, 26], 166: [235, 26], 167: [193, 26], 168: [151, 26], 169: [109, 26],
    170: [67, 26]}

node_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
    61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 90, 91,
    93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
    117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 135, 136, 138, 139, 141, 142,
    143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165,
    166, 167, 168, 169, 170]
occupied_node_ids = []
node_map = {0: [1, 14], 1: [0, 2, 15], 2: [1, 3, 16], 3: [2, 4, 17], 4: [3, 5, 18], 5: [4, 6, 19], 6: [5, 7, 20],
    7: [6, 8, 21], 8: [7, 9, 22], 9: [8, 10, 23], 10: [9, 11, 24], 11: [10, 12, 25], 12: [11, 13, 26], 13: [12, 27],
    14: [0, 15, 28], 15: [1, 14, 16, 29], 16: [2, 15, 17], 17: [3, 16, 18], 18: [4, 17, 19, 30], 19: [5, 18, 20, 31],
    20: [6, 19, 21], 21: [7, 20, 22], 22: [8, 21, 23, 32], 23: [9, 22, 24, 33], 24: [10, 23, 25], 25: [11, 24, 26],
    26: [12, 25, 27, 34], 27: [13, 26, 35], 28: [14, 29, 36], 29: [15, 28, 37], 30: [18, 31, 39], 31: [19, 30, 40],
    32: [22, 33, 42], 33: [23, 32, 43], 34: [26, 35, 45], 35: [27, 34, 46], 36: [28, 37, 48], 37: [29, 36, 49], 38: [],
    39: [30, 40, 52], 40: [31, 39, 53], 41: [], 42: [32, 43, 56], 43: [33, 42, 57], 44: [], 45: [34, 46, 60],
    46: [35, 45, 61], 47: [61], 48: [36, 49, 62], 49: [37, 48, 50, 63], 50: [49, 51, 64], 51: [50, 52, 65],
    52: [39, 51, 53, 66], 53: [40, 52, 54, 67], 54: [53, 55, 68], 55: [54, 56, 69], 56: [42, 55, 57, 70],
    57: [43, 56, 58, 71], 58: [57, 59, 72], 59: [58, 60, 73], 60: [45, 59, 61, 74], 61: [46, 47, 60, 75],
    62: [48, 63, 76], 63: [49, 62, 64, 77], 64: [50, 63, 65], 65: [51, 64, 66], 66: [52, 65, 67, 78],
    67: [53, 66, 68, 79], 68: [54, 67, 69], 69: [55, 68, 70], 70: [56, 69, 71, 80], 71: [57, 70, 72, 81],
    72: [58, 71, 73], 73: [59, 72, 74], 74: [60, 73, 75, 82], 75: [61, 74, 83], 76: [62, 77, 84], 77: [63, 76, 85],
    78: [66, 79, 87], 79: [67, 78, 88], 80: [70, 81, 90], 81: [71, 80, 91], 82: [74, 83, 93], 83: [75, 82, 94],
    84: [76, 85, 95], 85: [77, 84, 96], 86: [], 87: [78, 88, 99], 88: [79, 87, 100], 89: [], 90: [80, 91, 103],
    91: [81, 90, 104], 92: [], 93: [82, 94, 107], 94: [83, 93, 108], 95: [84, 96, 110], 96: [85, 95, 97, 111],
    97: [96, 98, 112], 98: [97, 99, 113], 99: [87, 98, 100, 114], 100: [88, 99, 101, 115], 101: [100, 102, 116],
    102: [101, 103, 117], 103: [90, 102, 104, 118], 104: [91, 103, 105, 119], 105: [104, 106, 120],
    106: [105, 107, 121], 107: [93, 106, 108, 122], 108: [94, 107, 123], 109: [123], 110: [95, 111, 124],
    111: [96, 110, 112, 125], 112: [97, 111, 113], 113: [98, 112, 114], 114: [99, 113, 115, 126],
    115: [100, 114, 116, 127], 116: [101, 115, 117], 117: [102, 116, 118], 118: [103, 117, 119, 128],
    119: [104, 118, 120, 129], 120: [105, 119, 121], 121: [106, 120, 122], 122: [107, 121, 123, 130],
    123: [108, 109, 122, 131], 124: [110, 125, 132], 125: [111, 124, 133], 126: [114, 127, 135], 127: [115, 126, 136],
    128: [118, 129, 138], 129: [119, 128, 139], 130: [122, 131, 141], 131: [123, 130, 142], 132: [124, 133, 143],
    133: [125, 132, 144], 134: [], 135: [126, 136, 147], 136: [127, 135, 148], 137: [], 138: [128, 139, 151],
    139: [129, 138, 152], 140: [], 141: [130, 142, 155], 142: [131, 141, 156], 143: [132, 144, 157],
    144: [133, 143, 145, 158], 145: [144, 146, 159], 146: [145, 147, 160], 147: [135, 146, 148, 161],
    148: [136, 147, 149, 162], 149: [148, 150, 163], 150: [149, 151, 164], 151: [138, 150, 152, 165],
    152: [139, 151, 153, 166], 153: [152, 154, 167], 154: [153, 155, 168], 155: [141, 154, 156, 169],
    156: [142, 155, 170], 157: [143, 158], 158: [144, 157, 159], 159: [145, 158, 160], 160: [146, 159, 161],
    161: [147, 160, 162], 162: [148, 161, 163], 163: [149, 162, 164], 164: [150, 163, 165], 165: [151, 164, 166],
    166: [152, 165, 167], 167: [153, 166, 168], 168: [154, 167, 169], 169: [155, 168, 170], 170: [156, 169]}
city_ids = [38, 41, 44, 86, 89, 92, 134, 137, 140]
city_gates = {38: [16, 17, 29, 30, 37, 39, 50, 51], 41: [20, 21, 31, 32, 40, 42, 54, 55],
    44: [24, 25, 33, 34, 43, 45, 58, 59], 86: [64, 65, 77, 78, 85, 87, 97, 98], 89: [68, 69, 79, 80, 88, 90, 101, 102],
    92: [72, 73, 81, 82, 91, 93, 105, 106], 134: [112, 113, 125, 126, 133, 135, 145, 146],
    137: [116, 117, 127, 128, 136, 138, 149, 150], 140: [120, 121, 129, 130, 139, 141, 153, 154]}

colours_list = {'aqua': (255, 255, 0), 'cream': (204, 223, 238), 'banana': (87, 207, 227), 'violet': (226, 43, 138),
    'pink': (180, 105, 255), 'tomato': (71, 99, 255), 'green': (159, 255, 84)}


def angle_correction(angle):
    if 180 >= angle >= 135:
        angle = 45+angle-360
    else:
        angle = 45+angle
    return angle


# get equations
def find_line_equation(a, b):
    x2, y2 = b[0], b[1]
    x1, y1 = a[0], a[1]
    if x2-x1 == 0:
        line_equation = [np.Inf, x1]
    else:
        m = (y2-y1) / (x2-x1)
        line_equation = [m, y1-(m * x1)]
    return line_equation


def find_line_angle(a, b):
    line_equation = find_line_equation(a, b)
    line_angle = int(np.degrees(np.arctan(line_equation[0])))
    if b[1] > a[1]:
        # line pointing below
        if line_angle > 0:
            line_angle = line_angle-180
    else:
        # line pointing upwards
        if line_angle < 0:
            line_angle = 180+line_angle
    if int(line_angle) in [180, -180, 0]:
        if b[0] > a[0]:
            line_angle = 180
        else:
            line_angle = 0
    return line_angle


def position_equality(a, b):
    x: bool = False
    y: bool = False
    if abs(a[0]-b[0]) < 10:
        x = True
    if abs(a[1]-b[1]) < 10:
        y = True
    if x and y:
        return True
    return False


def angle_equality(a, b):
    if abs(a-b) < 20 or abs(a-b) > 340:
        return True
    return False


def distance_between(a, b):
    d = int(np.sqrt((b[1]-a[1]) ** 2+(b[0]-a[0]) ** 2))
    return d


def angle_between(a, b):
    if a < 0:
        a = 360-a
    if b < 0:
        b = 360-b
    angle_diff = min(abs(a-b), 360-abs(a-b))
    return angle_diff


def dist_bw_pt_and_line(p, l):
    [m, c] = l
    [x, y] = p
    if m == np.Inf:
        dist = abs(x-c)
    else:
        dist = abs(m * x-y+c) / (np.sqrt(m ** 2+1))
    return dist


class Node:
    def __init__(self, id, parent):
        self.id = id
        for i in all_nodes:
            if i == self.id:
                self.pos = all_nodes[i]
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent
        self.children = node_map[self.id]


def find_astar_path(start, end):
    start_node = Node(start, None)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(end, None)
    end_node.g = end_node.h = end_node.f = 0
    if end in city_gates:
        gates = city_gates[end]
        """gate_nodes = []
        for i in gates:
            gate_nodes.append(Node(i, None))"""
    else:
        gates = [end]

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # we get one index and item that have lowest f
        open_list.pop(current_index)
        closed_list.append(current_node)
        # if we reach goal node
        if current_node.id in gates:
            path = []
            current = current_node
            while current is not None:
                path.append(current.id)
                current = current.parent
            path = path[::-1]
            return path

        children_ids = current_node.children
        for child_id in children_ids:
            child = Node(child_id, current_node)
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g+40
            child.h = abs((child.pos[0]-end_node.pos[0]))+abs((child.pos[1]-end_node.pos[1]))
            child.f = child.g+child.h

            # Child is already in the open list
            for open_node in open_list:
                if child.id == open_node.id and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def shorten_journey(path):
    short_journey = [path[0]]
    for i, node in enumerate(path):
        if i != 0 and i != len(path)-1:
            iup = all_nodes[path[i+1]]
            idown = all_nodes[path[i-1]]
            if abs(iup[0]-idown[0]) > 5 and abs(iup[1]-idown[1]) > 5:
                short_journey.append(node)
    short_journey.append(path[len(path)-1])
    return short_journey


class bot:
    id = 0
    color = ()
    position = [0, 0]
    angle: int = 0
    ip = "192.168.15."
    closest_node = 1
    # destination: [x, y]
    destination = []
    # journey: list of ids of coordinates on all_cells: [id1, id2, ...]
    journey = None
    # next target: id corresponding to coordinates in journey
    next_target = 0
    # next target angle: angle between bot position and next target position
    next_target_angle: int = 0

    found = False
    available = True
    reached = False

    speed = 255
    turn_speed = 255

    def __init__(self, id, color, ip):
        self.ip = self.ip+str(ip)
        self.color = color
        self.id = id  # print(str(self.id)+" : "+self.ip+" : "+self.color)

    # finds coordinates and updates position. writes the coordinates and angle of bot next to it
    def mark_bot(self, video_frame, video_frame2):
        x = self.position[0]
        y = self.position[1]
        cv2.putText(video_frame, str(self.position)+", "+str(self.angle), (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    colours_list[self.color], 2)
        cv2.putText(video_frame2, str(self.position)+", "+str(self.angle), (x+10, y-frame2_adjustment),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, colours_list[self.color], 2)

    # finds corners and updates closest node. also runs mark bot within
    def find_bot(self, corners, ids, corners2, ids2):
        if len(corners) > 0 or len(corners2) > 0:
            # flatten the ArUco IDs list
            ids = ids.flatten() if len(corners) else []
            ids2 = ids2.flatten() if len(corners2) else []
            # loop over the detected ArUCo corners
            if self.id in ids:
                for (markerCorner, markerID) in zip(corners, ids):
                    if self.id == markerID:
                        corners = markerCorner.reshape((4, 2))
                        (topLeft, topRight, bottomRight, bottomLeft) = corners
                        # convert each of the (x, y)-coordinate pairs to integers
                        topRight = (int(topRight[0]), int(topRight[1]))
                        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                        topLeft = (int(topLeft[0]), int(topLeft[1]))
                        x = int((topRight[0]+topLeft[0]+bottomRight[0]+bottomLeft[0]) / 4)
                        y = int((topRight[1]+topLeft[1]+bottomRight[1]+bottomLeft[1]) / 4)
                        angle = int(find_line_angle(topLeft, bottomRight))
                        self.position = [int(x), int(y)]
                        self.angle = angle_correction(angle)
                        self.found = True
                        for i in all_nodes:
                            if position_equality(all_nodes[i], self.position):
                                self.closest_node = i
                    else:
                        bot.found = False
            if self.id in ids2:
                for (markerCorner, markerID) in zip(corners2, ids2):
                    if self.id == markerID:
                        corners = markerCorner.reshape((4, 2))
                        (topLeft, topRight, bottomRight, bottomLeft) = corners
                        # convert each of the (x, y)-coordinate pairs to integers
                        topRight = (int(topRight[0]), int(topRight[1]))
                        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                        topLeft = (int(topLeft[0]), int(topLeft[1]))
                        x = int((topRight[0]+topLeft[0]+bottomRight[0]+bottomLeft[0]) / 4)
                        y = int((topRight[1]+topLeft[1]+bottomRight[1]+bottomLeft[1]) / 4)
                        angle = int(find_line_angle(topLeft, bottomRight))
                        y = y+frame2_adjustment
                        self.position = [int(x), int(y)]
                        self.angle = angle_correction(angle)
                        self.found = True
                        for i in all_nodes:
                            if position_equality(all_nodes[i], self.position):
                                self.closest_node = i
                    else:
                        bot.found = False
            for i, coords in enumerate(all_centers):
                if position_equality(coords, self.position):
                    self.closest_node = i

    # finds the path using a* pathfinding.
    def find_journey(self, end_pos):
        self.journey = find_astar_path(self.closest_node, end_pos)
        self.journey = shorten_journey(self.journey)
        self.reached = False

    # draws that path (if it exists) otherwise the previous path is kept on display
    def draw_journey(self, video_frame, video_frame2):
        if self.journey is not None:
            for i in range(len(self.journey)-1):
                id1 = self.journey[i]
                id2 = self.journey[i+1]
                x1, y1 = all_nodes[id1]
                x2, y2 = all_nodes[id2]
                cv2.line(video_frame, (x1, y1), (x2, y2), colours_list[self.color], 2)
                cv2.line(video_frame2, (x1, y1-frame2_adjustment), (x2, y2-frame2_adjustment), colours_list[self.color],
                         2)

    # loop backwards from the end to find the farthest target accessible through a straight line
    def find_next_target(self):
        for index, i in enumerate(self.journey):
            if self.closest_node == i:
                if index == len(self.journey)-1:
                    self.reached = True
                else:
                    self.next_target = self.journey[index+1]

    def draw_next_target(self, video_frame, video_frame2):
        next_target_coords = all_nodes[self.next_target]
        cv2.line(video_frame, self.position, next_target_coords, colours_list[self.color], 3)
        cv2.line(video_frame2, (self.position[0], self.position[1]-frame2_adjustment),
                 tuple([next_target_coords[0], next_target_coords[1]-frame2_adjustment]), colours_list[self.color], 3)
        cv2.putText(video_frame, str(self.next_target_angle), tuple(next_target_coords), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    colours_list[self.color], 2)
        cv2.putText(video_frame2, str(self.next_target_angle),
                    tuple([next_target_coords[0], next_target_coords[1]-frame2_adjustment]), cv2.FONT_HERSHEY_SIMPLEX,
                    1, colours_list[self.color], 2)

    def draw_path(self, video_frame, video_frame2):
        self.mark_bot(video_frame, video_frame2)
        self.draw_journey(video_frame, video_frame2)
        self.draw_next_target(video_frame, video_frame2)

    def send_command(self, arr):
        byte_message = bytes(str(arr), " utf-8")
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(byte_message, (str(self.ip), 4210))

    # [ejection, speedL, speedR, angle_to_turn]
    def stop(self):
        arr = [0, 0, 0, 0]
        self.send_command(arr)

    def go(self):
        arr = [0, self.speed, self.speed, 0]
        self.send_command(arr)

    def eject(self):
        arr = [1, 0, 0, 0]
        self.send_command(arr)
        time.sleep(1)

    def turn(self, angle):
        arr = [0, 0, 0, angle]
        self.send_command(arr)
        time.sleep(1+(abs(angle) / 60))

    def align(self):
        if angle_equality(self.angle, self.next_target_angle):
            self.go()
        else:
            self.stop()
            bt_angl = self.angle
            nt_angl = self.next_target_angle
            angle = angle_between(nt_angl, bt_angl)
            # turning positive is turning left
            if nt_angl > 0:
                if bt_angl > 0:
                    if bt_angl > nt_angl:
                        self.turn(angle)
                    else:
                        self.turn(-angle)
                else:
                    if bt_angl > -(180-nt_angl):
                        self.turn(-angle)
                    else:
                        self.turn(angle)
            else:
                if bt_angl > 0:
                    if bt_angl > 180+nt_angl:
                        self.turn(-angle)
                    else:
                        self.turn(angle)
                else:
                    if bt_angl > nt_angl:
                        self.turn(angle)
                    else:
                        self.turn(-angle)

    def run_bot(self, i, d):
        self.available = False
        d_node = cities[d]
        i_node = induct_stations[i]
        # find journey and next target
        self.find_journey(i_node)
        while not self.reached:
            self.find_next_target()
            self.align()
        self.stop()
        time.sleep(5)
        self.find_journey(d_node)
        while not self.reached:
            self.find_next_target()
            self.align()
        self.eject()
        self.available = True

    # def bot_fullcode(self, frame, frame2, corners, ids, corners2, ids2, ):


def draw_markers(corners, ids, frame):
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # draw the bounding box of the ArUCo detection
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the ArUco
            # marker
            cX = int((topLeft[0]+bottomRight[0]) / 2.0)
            cY = int((topLeft[1]+bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            # draw the ArUco marker ID on the image
            cv2.putText(frame, str(markerID), (cX-30, cY+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def draw_maps(video_frame1, video_frame2):
    j = 36
    for i in frame1_centers:
        cv2.rectangle(video_frame1, (i[0]-20, i[1]-20), (i[0]+20, i[1]+20), (255, 255, 0), 1)
        cv2.putText(video_frame1, str(j), (i[0], i[1]), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 255), 1)
        j += 1
    k = 0
    for i in frame2_centers:
        cv2.rectangle(video_frame2, (i[0]-20, i[1]-20-frame2_adjustment), (i[0]+20, i[1]+20-frame2_adjustment),
                      (255, 255, 0), 1)
        cv2.putText(video_frame2, str(k), (i[0], i[1]-frame2_adjustment), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 255), 1)
        k += 1


# 192.168.15.210 -- 0
# 192.168.15.158 -- 1
# 192.168.15.140 -- 2
# 192.168.15.249 -- 3
# 192.168.15.178 -- 4
# 192.168.15.126 -- 5
# 192.168.15.157 -- 7

bot0 = bot(0, 'aqua', "210")
bot1 = bot(1, 'cream', "158")
bot2 = bot(2, 'banana', "140")
bot3 = bot(3, 'violet', "249")
bot4 = bot(4, 'pink', "178")
bot5 = bot(5, 'tomato', "126")
bot7 = bot(7, 'green', "157")

df = pd.read_csv("packagedata.csv")
all_bots = [bot3]
cities = {'Jaipur': 38, 'Ahmedabad': 41, 'Pune': 44, 'Hyderabad': 86, 'Bengaluru': 89, 'Chennai': 92, 'Kolkata': 134,
    'Delhi': 137, 'Mumbai': 140}
bots_available = []
induct_stations = {1: 109, 2: 47}
n = 0

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()


def run_video():
    vid0 = cv2.VideoCapture(1)
    vid1 = cv2.VideoCapture(0)
    while True:
        ret, frame = vid0.read()
        ret2, frame2 = vid1.read()

        # modify frame 1
        (h, w) = frame.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), -2, 1.0)
        frame = cv2.warpAffine(frame, M, (w, h))
        frame = frame[75:390, 50:505]
        frame = cv2.resize(frame, (660, 460))
        frame = cv2.flip(frame, -1)

        # modify frame 2
        frame2 = cv2.flip(frame2, -1)
        frame2 = frame2[75:360, 110:600]
        frame2 = cv2.resize(frame2, (660, 379))

        # scan for all aruco markers, return tuple of (corners, ids, rejected)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
        (corners2, ids2, rejected2) = cv2.aruco.detectMarkers(frame2, arucoDict, parameters=arucoParams)

        # draw the markers found
        draw_markers(corners, ids, frame)
        draw_markers(corners2, ids2, frame2)

        draw_maps(frame, frame2)

        cv2.imshow('Frame', frame)
        cv2.imshow('Frame2', frame2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid0.release()
    vid1.release()
    cv2.destroyAllWindows()


def run_bots():
    while True:
        while len(bots_available) > 0:
            for index, bt in enumerate(bots_available):
                global n
                i = df['Induct Station'][n]
                d = df['Destination'][n]
                n = n+1
                bt.run_bot(i, d)
                print(str(bt.id)+" going to "+str(i)+", "+str(d))
                bots_available.pop(index)
                print(bots_available)


if __name__ == '__main__':
    a = Thread(target=run_video)
    a.start()
    b = Thread(target=run_bots)
    b.start()
