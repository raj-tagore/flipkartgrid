import cv2
import numpy as np

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
            cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1]-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                        2)
            print("[INFO] ArUco marker ID: {}".format(markerID))

vid0 = cv2.VideoCapture(1)
vid1 = cv2.VideoCapture(0)
while (True):
    ret, frame = vid0.read()
    ret2, frame2 = vid1.read()
    
    # modify frame 1
    (h, w) = frame.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -2, 1.0)
    frame = cv2.warpAffine(frame, M, (w, h))
    frame = frame[75:390, 50:500]
    frame = cv2.resize(frame, ((540-50), (390-75)))
    frame = cv2.flip(frame, -1)
    
    # modify frame 2
    frame2 = cv2.flip(frame2, -1)
    frame2 = frame2[75:360, 110:600]
    frame2 = cv2.resize(frame2, ((600-110), (360-75)))
    
    
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams) 
    (corners2, ids2, rejected2) = cv2.aruco.detectMarkers(frame2, arucoDict, parameters=arucoParams)
    
    draw_markers(corners, ids, frame)
    draw_markers(corners2, ids2, frame2)
    
    cv2.imshow('Frame', frame)
    cv2.imshow('Frame2', frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid0.release()
vid1.release()
cv2.destroyAllWindows()
