import cv2

"""image2 = cv2.imread("photo (1).jpg")

# crop image
print(image2.shape)
image2 = image2[60:970, 200:1820]
image2 = cv2.resize(image2, (866, 422))
image2 = cv2.flip(image2, 0)
cv2.imshow("Final Image", image2)
cv2.waitKey(0)

cv2.imshow("thresh", thresh)
cv2.waitKey(0)
cv2.imshow("Final Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""



import cv2

image2 = cv2.imread("map.png")
all_cells = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
             38, 39, 40, 41, 42, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74,
             75, 76, 77, 78, 79]
gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c = 0
viablecontours = []
for i in contours:
    area = cv2.contourArea(i)
    if area > 1000:
        viablecontours.append(c)
        #cv2.drawContours(image2, contours, c, (0, 255, 0), 3)
    c += 1
print(viablecontours)

all_centers = []
for i in all_cells:
    M = cv2.moments(contours[i])
    Cx = int(M["m10"] / M["m00"])
    Cy = int(M["m01"] / M["m00"])
    all_centers.append([Cx, Cy])
    cv2.drawContours(image2, contours, i, (0, 255, 0), 3)

cv2.imshow(str(22), image2)
cv2.waitKey(0)
