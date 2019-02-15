import cv2
import numpy as np

def ImgToNumpy(path):
        img = cv2.imread(path)
        return img


def ProcessImage(img):
        '''
        NOTE: Images must be only the map edges - no numbers or words
        '''        
        ## Convert to array, detect edges
        blurred = cv2.GaussianBlur(img, (3,3), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        edged1 = cv2.Canny(blurred, 50, 200, 255) ## Resultant array has 255 for edges and 0 for no edges
        kernel = np.ones((3,3),np.uint8)
        return cv2.dilate(edged1, kernel, iterations=3)

def DrawContours(img, cnt, index):
    cv2.drawContours(img, [cnt], index, (150,0,0), 3)

def DisplayImage(text, img, t=0):
    ## Diplay image
    cv2.imshow(text, img)
    cv2.waitKey(t)
    cv2.destroyAllWindows()

def FindContours(img):
        _,contours,_ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted(contours, key=cv2.contourArea, reverse=True)
        return contours


def GetRelevantContours(edges):
        ## returns all the convexhulls in following order: 
        ## outermost, inner contours
        ## requires manual handling
        '''
        TODO:
        [1] This function currently requires manual handling - we need to set the contours ourselves. 
        [2] Test whether convexhulls are adequate 
        '''
        # contours = FindContours(edges)        
        '''
        For pic_nolabel.jpg:
        contours[4] -- outer
        contours[5] -- inner
        cnt4 = [(20, 20),(20, 663),(1393, 663), (1393, 20)]
        cnt5 = [(97, 70), (97, 623), (1323, 623), (1323, 70)]        


        For simple.jpg:
        contours[1] -- outer
        contours[2] -- inner
        '''
        # print(len(contours))
        # cnt4 = cv2.convexHull(contours[4], False)
        # cnt5 = cv2.convexHull(contours[5], False)
        # DrawContours(edges, cnt5, -1)
        # DisplayImage('Canny', edged)
        '''
        ## pic_nolabel.jpg
        rec_coords = [
                [(20, 20),(20, 663),(1393, 663), (1393, 20)],
                [(97, 70), (97, 623), (1323, 623), (1323, 70)]
        ]
        '''
        rec_coords = [
                [(16, 16), (16, 567), (1676, 567), (1676, 16)],
                [(17, 17), (17, 115), (342, 115), (342, 17)],
                [(378, 17), (378, 115), (912, 115), (912, 17)],
                [(1092, 17), (1092, 115), (1511, 115), (1511, 17)],
                [(1546, 17), (1546, 115), (1676, 115), (1675, 17)],
                [(17, 141), (17, 447), (30, 447), (30, 141)],
                [(51, 141), (51, 447), (342, 447), (342, 141)],
                [(378, 141), (378, 447), (1059, 447), (1059, 141)],
                [(1092, 141), (1092, 447), (1570, 447), (1570, 141)],
                [(1597, 141), (1597, 447), (1675, 447), (1675, 141)],
                [(17, 468), (17, 566), (342, 566), (342, 468)],
                [(378, 468), (378, 566), (1675, 566), (1675, 468)]
        ]
        return rec_coords

def GetHoleCenterpoints(cnt):
        M = cv2.moments(cnt)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
        return cX, cY

def DrawLines(verts, img, thickness):
        # line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        for i in range(len(verts)-1):
                cv2.arrowedLine(img, verts[i], verts[i+1], (0, 0, 255), thickness)
        
        return img

def DrawCircles(points, img, thickness):
        # line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        for point in points:
                cv2.circle(img, point, 3, (0,0,0), thickness)
        return img

def OverlayImage(img, initial_img, a=0.6, b=2, c=0.):
        return cv2.addWeighted(initial_img, a, img, b, c)


## Testing functions ##
def FigureOutContours(path):
        img = ImgToNumpy(path)
        edged = ProcessImage(img)

        ## e5_4f_nolabel.jpg
        l = [
                [(16, 16), (16, 567), (1676, 567), (1676, 16)],
                [(17, 17), (17, 115), (342, 115), (342, 17)],
                [(378, 17), (378, 115), (912, 115), (912, 17)],
                [(1092, 17), (1092, 115), (1511, 115), (1511, 17)],
                [(1546, 17), (1546, 115), (1676, 115), (1675, 17)],
                [(17, 141), (17, 447), (30, 447), (30, 141)],
                [(51, 141), (51, 447), (342, 447), (342, 141)],
                [(378, 141), (378, 447), (1059, 447), (1059, 141)],
                [(1092, 141), (1092, 447), (1570, 447), (1570, 141)],
                [(1597, 141), (1597, 447), (1675, 447), (1675, 141)],
                [(17, 468), (17, 566), (342, 566), (342, 468)],
                [(378, 468), (378, 566), (1675, 566), (1675, 468)]
        ]

        ## pic_nolabel.jpg
        # l = [
        #         [(20, 20),(1393, 663)],
        #         [(95, 70), (1323, 623)],
        # ]
        for index in l: 
                cv2.rectangle(edged, (index[0][0],index[0][1]), (index[2][0], index[2][1]), (150,0,0), 2)

        DisplayImage("ConvexHulls", edged)

def TestContours(path):
        img = ImgToNumpy(path)
        edged = ProcessImage(img)
        GetRelevantContours(edged)
        DisplayImage("img", edged)

## for debugging only
# TestContours("../data/simple.jpg")
# FigureOutContours("../data/e5_4f_nolabel.jpg")

## Just draw the image {to get coords}




