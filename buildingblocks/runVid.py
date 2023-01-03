import cv2
import time

centers = [[754, 393], [711, 393], [666, 393], [622, 393], [578, 393], [536, 393], [495, 393], [453, 393], [411, 393],
           [370, 393],
           [328, 393], [284, 393], [242, 393], [198, 393], [154, 393], [109, 393], [754, 351], [711, 351], [666, 351],
           [622, 351],
           [578, 351], [536, 351], [494, 351], [453, 351], [411, 351], [369, 351], [328, 351], [284, 351], [241, 351],
           [198, 351],
           [154, 351], [109, 351], [495, 310], [453, 311], [411, 311], [370, 311], [495, 270], [453, 270], [411, 270],
           [369, 270],
           [495, 228], [453, 228], [411, 228], [369, 228], [453, 186], [411, 186], [495, 186], [369, 186], [495, 143],
           [453, 143],
           [411, 143], [495, 101], [453, 101], [411, 101], [370, 101], [495, 61], [453, 61], [411, 61], [370, 61]]


def draw_map(video_frame):
    j = 0
    for i in centers:
        cv2.rectangle(video_frame, (i[0] - 20, i[1] - 20), (i[0] + 20, i[1] + 20), (0, 255, 0), 1)
        cv2.putText(frame, str(j), (i[0], i[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        j += 1


if __name__ == '__main__':

    safety_frame = [[[]]]

    vid0 = cv2.VideoCapture("http://192.168.15.248:8080/video")

    while True:

        t0 = t1 = t2 = t3 = t4 = time.time()

        ret, frame = vid0.read()

        try:
            frame = frame[30:940, 100:1900]
            frame = cv2.resize(frame, (866, 422))
            frame = cv2.flip(frame, -1)

            t1 = time.time()

            draw_map(frame)

            t2 = time.time()

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
            break

        times = [t1 - t0, t2 - t0]
        total = 0
        for i in times:
            total = total + i
        print(total)

    vid0.release()
    cv2.destroyAllWindows()
