import cv2
import numpy as np

def ProcessImage(path):
        ## Read in image
        img_large = cv2.imread(path)
        img = cv2.resize(img_large, (0,0), fx=1, fy=1)
        # Assume that the image is already grayscale

        ## Convert to array, detect edges
        blurred = cv2.GaussianBlur(img, (3,3), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        edged1 = cv2.Canny(blurred, 50, 200, 255) ## Resultant array has 255 for edges and 0 for no edges
        kernel = np.ones((3,3),np.uint8)
        return cv2.dilate(edged1, kernel, iterations=3)

def DrawContours(img, cnt, index):
    cv2.drawContours(img, [cnt], index, (150,0,0), 3)


def DisplayImage(text, img):
    ## Diplay image
    cv2.imshow(text, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def GetRelevantContours(edges):
        ## returns all the contours in following order: 
        ## outermost, inner contours
        _,contours,_ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted(contours, key=cv2.contourArea, reverse=True)
        
        '''
        For pic_nolabel.jpg:
        contours[4] -- outer
        contours[5] -- inner

        For simple.jpg:
        contours[1] -- outer
        contours[2] -- inner
        '''
        # print(len(contours))
        cnt4 = cv2.convexHull(contours[4], False)
        cnt5 = cv2.convexHull(contours[5], False)
        # DrawContours(edges, contours[2], -1)
        # DisplayImage('Canny', edged)
        return cnt4, cnt5


## for debugging only
# edged = ProcessImage("data/simple.jpg")
# GetRelevantContours(edged)

