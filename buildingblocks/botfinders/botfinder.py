import cv2
import numpy as np

image2 = cv2.imread("photo (2).jpg")
image2 = image2[60:940, 130:1870]
image2 = cv2.resize(image2, (866, 422))
image2 = cv2.flip(image2, -1)

cv2.imshow("Final Image", image2)
cv2.waitKey(0)

hsv = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 150, 150])
upper_red = np.array([25, 255, 255])

mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(image2, image2, mask=mask)

gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
# make thresh
thresh = cv2.adaptiveThreshold(gray, 225, 1, 1, 19, 2)
# find all contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image2, contours, 0, (0, 255, 0), 3)

(x,y),(MA,ma),angle = cv2.fitEllipse(contours[0])
print(x, y, angle)

cv2.imshow("Final Image", gray)
cv2.waitKey(0)

cv2.imshow("Final Image", thresh)
cv2.waitKey(0)

cv2.imshow("Final Image", image2)
cv2.waitKey(0)