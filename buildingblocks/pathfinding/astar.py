
all_centers = ac = [[614,569],[572,569],[530,569],[488,569],[445,569],[404,569],[361,569],[320,569],[277,569],
        [235,569],[193,569],[151,569],[109,569],[67,569],[614,527],[572,527],[530,527],[488,527],[445,527],[404,527],
        [361,527],[320,527],[277,527],[235,527],[193,527],[151,527],[109,527],[67,527],[614,485],[572,485],[445,485],
        [404,485],[276,485],[235,485],[109,485],[66,485],[613,443],[572,443],[509,465],[445,443],[403,443],[340,465],
        [277,443],[235,443],[173,465],[109,443],[67,443],[26,402],[614,402],[572,402],[530,402],[488,402],[445,402],
        [404,402],[361,402],[320,402],[277,402],[235,402],[193,402],[151,402],[109,402],[67,402],[614,360],[572,360],
        [530,360],[488,360],[445,360],[404,360],[361,360],[320,360],[277,360],[235,360],[193,360],[151,360],[109,360],
        [67,360],[614,318],[572,318],[445,318],[404,318],[276,318],[235,318],[109,318],[67,318],[613,276],[572,276],
        [509,298],[445,276],[404,276],[340,298],[277,276],[235,276],[173,298],[109,276],[67,276],[614,235],[572,235],
        [530,235],[488,235],[445,235],[404,235],[361,235],[320,235],[277,235],[235,235],[193,235],[151,235],[109,235],
        [67,235],[26,193],[614,193],[572,193],[530,193],[488,193],[445,193],[404,193],[361,193],[320,193],[277,193],
        [235,193],[193,193],[151,193],[109,193],[67,193],[614,151],[572,151],[445,151],[404,151],[277,151],[235,151],
        [109,151],[67,151],[614,109],[572,109],[509,131],[445,109],[404,109],[340,131],[277,109],[235,109],[173,131],
        [109,109],[67,109],[614,68],[572,68],[530,68],[488,68],[445,68],[404,68],[361,68],[320,68],[277,68],[235,68],
        [193,68],[151,68],[109,68],[67,68],[614,26],[572,26],[530,26],[488,26],[445,26],[404,26],[361,26],[320,26],
        [277,26],[235,26],[193,26],[151,26],[109,26],[67,26]]
frame1_centers = all_centers[37:172]
frame2_centers = all_centers[0:110]
frame2_adjustment = -220
all_nodes = []
node_ids = []
node_map = {}
city_ids = []
city_gates = {38: [16, 17, 29, 30, 37, 39, 50, 51], 41: [20, 21, 31, 32, 40, 42, 54, 55],
    44: [24, 25, 33, 34, 43, 45, 58, 59], 86: [64, 65, 77, 78, 85, 87, 97, 98], 89: [68, 69, 79, 80, 88, 90, 101, 102],
    92: [72, 73, 81, 82, 91, 93, 105, 106], 134: [112, 113, 125, 126, 133, 135, 145, 146],
    137: [116, 117, 127, 128, 136, 138, 149, 150], 140: [120, 121, 129, 130, 139, 141, 153, 154]}

class Node:
    def __init__(self, id, parent):
        self.id = id
        for i in all_nodes:
            if i[2] == self.id:
                self.pos = [i[0], i[1]]
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
    gates = city_gates[end]
    gate_nodes = []
    for i in gates:
        gate_nodes.append(Node(i, None))

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list)>0:
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

def form_short_path(path):
    short_journey = [path[0]]
    for i, node in enumerate(path):
        if i != 0 and i != len(path)-1:
            iup = all_nodes[path[i+1]]
            idown = all_nodes[path[i-1]]
            if abs(iup[0]-idown[0]) > 5 and abs(iup[1]-idown[1]) > 5:
                short_journey.append(node)
    short_journey.append(path[len(path)-1])
    return short_journey

def form_node_map():
    j = 0
    for i in all_centers:
        i.append(j)
        node_ids.append(j)
        all_nodes.append(i)
        node_map[j] = []
        j = j+1

    for i in node_ids:
        n = all_nodes[i]
        for j in node_ids:
            m = all_nodes[j]
            if abs(m[0]-n[0])<44 and abs(m[1]-n[1])<44:
                if abs(m[0]-n[0])<=10 or abs(m[1]-n[1])<=10:
                    if j!=i:
                        node_map[i].append(j)

    #print(node_map[63])
    node_ids.remove(140)
    node_ids.remove(137)
    node_ids.remove(134)
    node_ids.remove(92)
    node_ids.remove(89)
    node_ids.remove(86)
    node_ids.remove(44)
    node_ids.remove(41)
    node_ids.remove(38)
    city_ids = [38, 41, 44, 86, 89, 92, 134, 137, 140]
    print(all_nodes)
    print(node_ids)
    print(node_map)
    print(city_ids)

if __name__ == '__main__':
    form_node_map()
    path = find_astar_path(2, 44)
    print(path)
    print(form_short_path(path))

