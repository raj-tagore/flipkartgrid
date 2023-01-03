import socket
import cv2
import numpy as np
import time
from threading import Thread

all_centers = [[754, 393], [711, 393], [666, 393], [622, 393], [578, 393], [536, 393], [495, 393], [453, 393],
    [411, 393], [370, 393], [328, 393], [284, 393], [242, 393], [198, 393], [154, 393], [109, 393], [754, 351],
    [711, 351], [666, 351], [622, 351], [578, 351], [536, 351], [494, 351], [453, 351], [411, 351], [369, 351],
    [328, 351], [284, 351], [241, 351], [198, 351], [154, 351], [109, 351], [495, 310], [453, 311], [411, 311],
    [370, 311], [495, 270], [453, 270], [411, 270], [369, 270], [495, 228], [453, 228], [411, 228], [369, 228],
    [453, 186], [411, 186], [495, 186], [369, 186], [495, 143], [453, 143], [411, 143], [495, 101], [453, 101],
    [411, 101], [370, 101], [495, 61], [453, 61], [411, 61], [370, 61], [370, 61+84], [754+42, 393], [109-42, 393],
    [754+42, 351], [109-42, 351], [495, 19], [453, 19], [411, 19], [370, 19], [754+42, 372], [109-42, 372],
    [516, 61-42], [370-21, 61-42], [391, 61-42], [432, 61-42]]

current_bot = 0


# finding equation and angle for any line using 2 coordinates

def find_line_equation(a, b):
    x2, y2 = b[0], b[1]
    x1, y1 = a[0], a[1]
    if x2-x1 == 0:
        line_equation = [np.Inf, y1]
    else:
        line_equation = [(y2-y1) / (x2-x1), y1]
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


# Draw the map over the image, using the "all cells" array derived from map2.png

def draw_map(video_frame):
    j = 0
    for i in all_centers:
        cv2.rectangle(video_frame, (i[0]-20, i[1]-20), (i[0]+20, i[1]+20), (0, 255, 0), 1)
        cv2.putText(video_frame, str(j), (i[0], i[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        j += 1


# checking equality

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


def position_equality(a, b):
    x: bool = False
    y: bool = False
    if abs(a[0]-b[0]) < 30:
        x = True
    if abs(a[1]-b[1]) < 30:
        y = True
    if x and y:
        return True
    return False


def angle_equality(a, b):
    if abs(a-b) < 20 or abs(a-b) > 340:
        return True
    return False


# the "bot" class

class bot:
    position = [0, 0]
    angle: int = 0
    destination = []
    journey = [58, 25, 31, 25, 58]
    path_equations = [[]]
    next_target = 0
    next_target_angle = 0
    ip = "192.168.15."
    speed = 0
    delay_before = 0.15
    delay_after = 0.15
    turn_speed = 0
    turn_delay_before = 0.15
    turn_delay_after = 0.15
    color_range = []
    color = " "
    ejected = False

    def __init__(self, ip, color, journey):
        self.ip = self.ip+str(ip)
        print(self.ip)
        self.color = color
        self.journey = journey

    def p_control_speed(self):
        next_target_coords = all_centers[self.journey[self.next_target]]
        if distance_between(self.position, next_target_coords) > 50:
            self.speed = 190
            self.delay_before = 0.2
            self.delay_after = 0.2
        elif distance_between(self.position, next_target_coords) <= 50:
            self.speed = 190
            self.delay_before = 0.15
            self.delay_after = 0.3

    def p_control_angle(self):
        if angle_between(self.angle, self.next_target_angle) > 60:
            self.turn_speed = 180
            self.turn_delay_before = 0.1
            self.turn_delay_after = 0.2
        elif angle_between(self.angle, self.next_target_angle) <= 60:
            self.turn_speed = 180
            self.turn_delay_before = 0.1
            self.turn_delay_after = 0.3

    def update_color_range(self):
        if self.color == 'red':
            self.color_range = [[0, 150, 150], [6, 255, 230]]
        elif self.color == 'blue':
            self.color_range = [[50, 150, 100], [100, 250, 250]]
        elif self.color == 'orange':
            self.color_range = [[10, 150, 150], [20, 250, 250]]
        elif self.color == 'violet':
            self.color_range = [[140, 50, 100], [165, 190, 250]]
        else:
            print("WRONG COLOR")

    def send_command(self, arr):
        byte_message = bytes(str(arr), " utf-8")
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(byte_message, (str(self.ip), 4210))

    def stop(self):
        arr = ['z', 0, 0]
        self.send_command(arr)

    def go(self):
        self.p_control_speed()
        arr = ['z', self.speed, -self.speed]
        self.send_command(arr)
        time.sleep(self.delay_before)
        self.stop()
        time.sleep(self.delay_after)
        print("go")

    def eject(self):
        arr = ['e', 0, 0]
        self.send_command(arr)
        time.sleep(1)

    def turn(self, direction):
        arr = ['z', 0, 0]
        self.p_control_angle()
        if direction:
            # turn right
            arr[2] = -self.turn_speed
            arr[1] = -self.turn_speed
            self.send_command(arr)
            time.sleep(self.turn_delay_before)
            self.stop()
            time.sleep(self.turn_delay_after)
            print("right")
        else:
            # turn left
            arr[2] = self.turn_speed
            arr[1] = self.turn_speed
            self.send_command(arr)
            time.sleep(self.turn_delay_before)
            self.stop()
            time.sleep(self.turn_delay_after)
            print("left")

    def find_bot(self, video_frame):
        hsv = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)
        self.update_color_range()
        lower_lt = np.array(self.color_range[0])
        upper_lt = np.array(self.color_range[1])

        mask = cv2.inRange(hsv, lower_lt, upper_lt)
        res = cv2.bitwise_and(video_frame, video_frame, mask=mask)
        # grayscale
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # make thresh
        thresh = cv2.adaptiveThreshold(gray, 225, 1, 1, 19, 2)
        # find all contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda i: cv2.contourArea(i), reverse=True)
        areas = []
        for i in contours:
            areas.append(cv2.contourArea(i))
        marker_locations = []
        for i in [contours[1], contours[2]]:
            (x, y), (_, _), angle = cv2.minAreaRect(i)
            marker_locations.append([x, y, angle])

        x = (marker_locations[0][0]+marker_locations[1][0]) / 2
        y = (marker_locations[0][1]+marker_locations[1][1]) / 2
        angle = find_line_angle(marker_locations[1], marker_locations[0])

        cv2.drawContours(video_frame, contours, 1, (0, 0, 255), 3)
        cv2.drawContours(video_frame, contours, 2, (0, 0, 255), 3)
        text_to_show = str(int(x))+', '+str(int(y))+', '+str(int(angle))
        cv2.putText(video_frame, text_to_show, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        self.position = [int(x), int(y)]
        self.angle = int(angle)

    def find_next_target(self, video_frame):
        if self.next_target <= len(self.journey)-1:
            next_target_coords = all_centers[self.journey[self.next_target]]
            cv2.line(video_frame, tuple(self.position), tuple(next_target_coords), (0, 255, 255), 3)
            if position_equality(self.position, next_target_coords):
                self.next_target += 1
                time.sleep(1)

    def find_next_angle(self, video_frame):
        if self.next_target <= len(self.journey)-1:
            next_target_coords = all_centers[self.journey[self.next_target]]
            self.next_target_angle = find_line_angle(self.position, next_target_coords)
            cv2.putText(video_frame, str(self.next_target_angle), tuple(next_target_coords), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)

    def find_path(self, video_frame):
        # find next target and angle
        self.find_next_target(video_frame)
        self.find_next_angle(video_frame)

    def align(self):
        b = self.angle
        p = self.next_target_angle
        if angle_equality(self.angle, self.next_target_angle):
            self.stop()
            return True
        else:
            if p > 0:
                if b > 0:
                    if b > p:
                        self.turn(0)
                    else:
                        self.turn(1)
                else:
                    if b > -(180-p):
                        self.turn(1)
                    else:
                        self.turn(0)
            else:
                if b > 0:
                    if b > 180+p:
                        self.turn(1)
                    else:
                        self.turn(0)
                else:
                    if b > p:
                        self.turn(0)
                    else:
                        self.turn(1)
        return False


# args = (ip, color, journey)
bot_red = bot(249, 'red', [35, 63, 25, 71])
bot_blue = bot(114, 'blue', [34, 69, 34, 72])
bot_violet = bot(178, 'violet', [33, 68, 33, 73])
bot_orange = bot(197, 'orange', [22, 62, 22, 64])

all_bots = [bot_red, bot_blue, bot_violet, bot_orange]


# live_bot = bot_orange


def run_video():
    safety_frame = [[[]]]

    vid0 = cv2.VideoCapture("http://192.168.15.248:8080/video")

    while True:
        global current_bot
        live_bot = all_bots[current_bot]

        ret, frame = vid0.read()

        try:
            frame = frame[30:940, 100:1900]
            frame = cv2.resize(frame, (866, 422))
            frame = cv2.flip(frame, -1)

            # mask the unwanted region of map
            mask1 = np.zeros(frame.shape[:2], dtype="uint8")
            cv2.rectangle(mask1, (50, 0), (820, 430), 255, -1)
            frame = cv2.bitwise_and(frame, frame, mask=mask1)

            live_bot.find_bot(frame)

            draw_map(frame)
            live_bot.find_path(frame)

            if ret:
                safety_frame = frame

            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        except cv2.Error:
            print("saved")
            safety_frame = safety_frame[60:940, 130:1870]
            safety_frame = cv2.resize(safety_frame, (866, 422))
            cv2.imshow('Frame', safety_frame)
            cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            live_bot.stop()
            break

    vid0.release()
    cv2.destroyAllWindows()


def run_bot():
    print("started ")
    while True:
        global current_bot
        live_bot = all_bots[current_bot]
        if live_bot.next_target == 2 and live_bot.ejected == False:
            live_bot.eject()
            live_bot.ejected = True
        elif live_bot.next_target >= len(live_bot.journey):
            live_bot.stop()
            current_bot = current_bot+1
            print("current bot: "+str(current_bot))
        else:
            k = live_bot.align()

            if k:
                live_bot.go()


if __name__ == '__main__':
    a = Thread(target=run_video)
    b = Thread(target=run_bot)
    a.start()
    b.start()
