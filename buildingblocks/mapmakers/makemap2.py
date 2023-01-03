
import cv2

image2 = cv2.imread("map2.png")
gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c = 0
viablecontours = []
for i in contours:
    area = cv2.contourArea(i)
    if area > 1000:
        viablecontours.append(c)
        cv2.drawContours(image2, contours, c, (0, 255, 0), 3)
    c += 1
print(viablecontours)
all_centers = []
for i in viablecontours:
    M = cv2.moments(contours[i])
    Cx = int(M["m10"] / M["m00"])
    Cy = int(M["m01"] / M["m00"])
    all_centers.append([Cx, Cy])
    cv2.drawContours(image2, contours, i, (0, 255, 0), 3)
print(all_centers)
j = 0
for i in all_centers:
    cv2.circle(image2, i, 7, (255, 255, 255), -1)
    cv2.putText(image2, str(j), [i[0]-10, i[1]-10], cv2.FONT_HERSHEY_COMPLEX, 0.25, (0, 0, 0), 1)
    j += 1

cv2.imshow(str(22), image2)
cv2.waitKey(0)
