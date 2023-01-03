import cv2

safetyframe = [[[]]]
vid0 = cv2.VideoCapture("http://192.168.15.248:8080/video")
while (True):
    ret, frame = vid0.read()
    if ret == True:
        safetyframe = frame
    try:
        frame = frame[60:940, 130:1870]
        frame = cv2.resize(frame, (866, 422))
        frame = cv2.flip(frame, 0)
        cv2.imshow('Frame', frame)
        cv2.waitKey(5)
    except cv2.error:
        cv2.imshow('Frame', safetyframe)
        cv2.waitKey(5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid0.release()
cv2.destroyAllWindows()

