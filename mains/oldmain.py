import socket
import cv2
import numpy as np
import time

all_cells = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
             36, 37, 38, 39, 40, 41, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71,
             72, 73, 74, 75, 76, 77, 78]

all_centers = []


# finding equation and angle for any line using 2 coordinates

def find_line_equation(a, b):
    x2, y2 = b[0], b[1]
    x1, y1 = a[0], a[1]
    if x2 - x1 == 0:
        line_equation = [np.Inf, y1]
    else:
        line_equation = [(y2 - y1) / (x2 - x1), y1]
    return line_equation


def find_line_angle(a, b):
    line_equation = find_line_equation(a, b)
    line_angle = int(np.degrees(np.arctan(line_equation[0])))
    if b[1] > a[1]:
        # line pointing below
        if line_angle > 0:
            line_angle = line_angle - 180
    else:
        # line pointing upwards or right/left
        if line_angle < 0:
            line_angle = 180 + line_angle
    return line_angle


# Draw the map over the image, using the "all cells" array derived from map2.png

def draw_map(video_frame):
    j = 0
    for i in all_cells:
        cv2.drawContours(video_frame, contours, i, (0, 255, 0), 1)
        # third argument is the ID of contours to be drawn
        # "contours" is the only array with the contours, the rest are just IDs mapping to "contours" array
    for i in all_centers:
        cv2.putText(frame, str(j), [i[0], i[1]], cv2.FONT_HERSHEY_COMPLEX, 0.25, (255, 255, 255), 1)
        j += 1


# checking equality

def position_equality(a, b):
    x: bool = False
    y: bool = False
    if abs(a[0] - b[0]) < 20:
        x = True
    if abs(a[1] - b[1]) < 20:
        y = True
    if x and y:
        return True
    return False


def angle_equality(a, b):
    if abs(a - b) < 20 or abs(a - b) > 340:
        return True
    return False


def angle_equality_2(a, b):
    if abs(a - b) < 10 or abs(a - b) > 350:
        return True
    return False


def wait(amount, start_time):
    now = time.time()
    if now - start_time >= amount:
        return True
    return False


# the "bot" class

class bot:
    position = []
    angle: int = 0
    destination = []
    journey = [58, 9, 6, 55, 58]
    path_equations = [[]]
    next_target = 2
    next_target_angle = 0
    rms = 0
    lms = 0
    ip = "192.168.15.249"
    speed = 250
    turn_speed = 225

    def send_command(self, arr):
        byte_message = bytes(str(arr), " utf-8")
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(byte_message, (str(self.ip), 4210))

    def stop(self):
        arr = ['z', 0, 0]
        self.send_command(arr)

    def go(self):
        arr = ['z', self.speed, -self.speed]
        self.send_command(arr)
        time.sleep(0.2)
        self.stop()

    def turn(self, direction):
        arr = ['z', 0, 0]
        if direction:
            # turn right
            arr[2] = -self.turn_speed
            arr[1] = -self.turn_speed
            self.send_command(arr)
            time.sleep(0.1)
            self.stop()
            print("right")
        else:
            # turn left
            arr[2] = self.turn_speed
            arr[1] = self.turn_speed
            self.send_command(arr)
            time.sleep(0.1)
            self.stop()
            print("left")

    def find_bot(self, video_frame):
        hsv = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 150, 150])
        upper_red = np.array([10, 255, 230])

        mask = cv2.inRange(hsv, lower_red, upper_red)
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

        x = (marker_locations[0][0] + marker_locations[1][0]) / 2
        y = (marker_locations[0][1] + marker_locations[1][1]) / 2
        angle = find_line_angle(marker_locations[1], marker_locations[0])

        cv2.drawContours(video_frame, contours, 1, (0, 0, 255), 3)
        cv2.drawContours(video_frame, contours, 2, (0, 0, 255), 3)
        text_to_show = str(int(x)) + ', ' + str(int(y)) + ', ' + str(int(angle))
        cv2.putText(video_frame, text_to_show, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        self.position = [int(x), int(y)]
        self.angle = int(angle)

        return self.position, self.angle

    def find_next_target(self, video_frame):
        next_target_coords = all_centers[self.journey[self.next_target]]
        cv2.line(video_frame, tuple(self.position), tuple(next_target_coords), (0, 255, 255), 3)
        if position_equality(self.position, next_target_coords):
            self.next_target += 1

    def find_next_angle(self, video_frame):
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
            print(self.angle)
            print(self.next_target_angle)
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
                    if b > -(180 - p):
                        self.turn(1)
                    else:
                        self.turn(0)
            else:
                if b > 0:
                    if b > 180 + p:
                        self.turn(1)
                    else:
                        self.turn(0)
                else:
                    if b > p:
                        self.turn(0)
                    else:
                        self.turn(1)
        print(p)
        print(b)
        return False


if __name__ == '__main__':

    safety_frame = [[[]]]

    image = cv2.imread("map2.png")

    # convert to pure B/W
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # make thresh
    thresh = cv2.adaptiveThreshold(gray, 225, 1, 1, 19, 2)
    # find all contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in all_cells:
        M = cv2.moments(contours[i])
        Cx = int(M["m10"] / M["m00"])
        Cy = int(M["m01"] / M["m00"])
        all_centers.append([Cx, Cy])

    bot_red = bot()

    vid0 = cv2.VideoCapture("http://192.168.15.248:8080/video")

    while True:

        t0 = t1 = t2 = t3 = t4 = time.time()

        ret, frame = vid0.read()

        try:
            frame = frame[30:940, 100:1900]
            frame = cv2.resize(frame, (866, 422))
            frame = cv2.flip(frame, -1)

            t1 = time.time()

            bot_red.find_bot(frame)

            t2 = time.time()

            draw_map(frame)
            bot_red.find_path(frame)

            t3 = time.time()

            k = bot_red.align()

            if k:
                bot_red.go()

            if ret:
                safety_frame = frame

            cv2.imshow('Frame', frame)
            cv2.waitKey(1)

        except cv2.Error:
            print("saved")
            safety_frame = safety_frame[60:940, 130:1870]
            safety_frame = cv2.resize(safety_frame, (866, 422))
            # cv2.imshow('Frame', safety_frame)
            # cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            bot_red.stop()
            break

        times = [t1 - t0, t2 - t0, t3 - t0, t4 - t0]
        total = 0
        for i in times:
            total = total + i
        print(total)

    vid0.release()
    cv2.destroyAllWindows()
