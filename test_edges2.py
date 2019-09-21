import cv2
import numpy as np
from matplotlib import pyplot as plt

kernel = np.ones((5,5),np.uint8)

img = cv2.imread('/home/john/Pictures/testing_image.png', 1)

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

LAND_MIN = np.array([26, 0, 20])
LAND_MAX = np.array([28, 100, 255])

SHALLOW_BOUND_MIN = np.array([20, 100, 100])
SHALLOW_BOUND_MAX = np.array([22, 255, 255])

HI_DEPTH_MIN = np.array([0, 0, 250])
HI_DEPTH_MAX = np.array([5, 255, 255])

MED_DEPTH_MIN = np.array([89, 0, 100])
MED_DEPTH_MAX = np.array([92, 100, 255])

WATER_BOUND_MIN = np.array([101, 100, 100])
WATER_BOUND_MAX = np.array([103, 255, 255])

LO_DEPTH_MIN = np.array([93, 0, 100])
LO_DEPTH_MAX = np.array([95, 150, 255])

SHALLOW_DEPTH_MIN = np.array([56, 0, 100])
SHALLOW_DEPTH_MAX = np.array([58, 150, 255])

TRAFFIC_MIN1 = np.array([150, 10, 10])
TRAFFIC_MAX1 = np.array([151, 255, 255])

low = np.array([150,10,10])
high = np.array([151,255,255])

trafficMask = cv2.inRange(hsv_img, TRAFFIC_MIN1, TRAFFIC_MAX1)






#contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contours, -1, (0,255,0), 3)






#FIND CONTOURS
landMask = cv2.inRange(hsv_img, LAND_MIN, LAND_MAX)
land_contour, land_hierarchy = cv2.findContours(landMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

shallowMask = cv2.inRange(hsv_img,SHALLOW_DEPTH_MIN, SHALLOW_DEPTH_MAX)
shallowBorderMask = cv2.inRange(hsv_img, SHALLOW_BOUND_MIN, SHALLOW_BOUND_MAX)
shallowMaskAll = cv2.bitwise_or(shallowMask, shallowBorderMask)
shallow_contour, shallow_hierarchy = cv2.findContours(shallowMaskAll, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

lowMask = cv2.inRange(hsv_img, LO_DEPTH_MIN, LO_DEPTH_MAX)
low_contour, low_hierarchy = cv2.findContours(lowMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

medMask = cv2.inRange(hsv_img, MED_DEPTH_MIN, MED_DEPTH_MAX)
medBorderMask = cv2.inRange(hsv_img, WATER_BOUND_MIN, WATER_BOUND_MAX)
medMaskAll = cv2.bitwise_or(medMask, medBorderMask)
medMaskNoGaps = cv2.morphologyEx(medMaskAll, cv2.MORPH_CLOSE, kernel)
med_contour, med_hierarchy = cv2.findContours(medMaskNoGaps, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

highMask = cv2.inRange(hsv_img, HI_DEPTH_MIN, HI_DEPTH_MAX)
high_contour, high_hierarchy = cv2.findContours(highMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

test = cv2.bitwise_or(highMask, medMaskNoGaps)


or1 = cv2.bitwise_or(shallowMask, lowMask)
or2 = cv2.bitwise_or(or1, medMask)
or3 = cv2.bitwise_or(or2,highMask)
or4 = cv2.bitwise_or(or3,landMask)

obstacles = cv2.bitwise_not(or4)

#med_depth = cv2.morphologyEx(med_depth, cv2.MORPH_OPEN, kernel)


#not1 = cv2.bitwise_not(and1)

plt.imshow(test,cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
