import cv2
import pyclipper as pyc
import matplotlib.pyplot as plt
import matplotlib.tri as tr
import numpy as np
from scipy.spatial import Delaunay
import random
import triangle as tr

def rect_contains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

def draw_delaunay(img, subdiv, delaunay_color ) :
 
    triangleList = subdiv.getTriangleList();
    size = img.shape
    r = (0, 0, size[1], size[0])
 
    for t in triangleList :
         
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
         
        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
         
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
 
 
# Draw voronoi diagram
def draw_voronoi(img, subdiv) :
 
    ( facets, centers) = subdiv.getVoronoiFacetList([])
 
    for i in xrange(0,len(facets)) :
        ifacet_arr = []
        for f in facets[i] :
            ifacet_arr.append(f)
         
        ifacet = np.array(ifacet_arr, np.int)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
 
        cv2.fillConvexPoly(img, ifacet, color, cv2.LINE_AA, 0)
        ifacets = np.array([ifacet])
        cv2.polylines(img, ifacets, True, (0, 0, 0), 1, cv2.LINE_AA, 0)
        cv2.circle(img, (centers[i][0], centers[i][1]), 3, (0, 0, 0), cv2.FILLED, cv2.LINE_AA, 0)

def DrawImage(polygons):
        for i in range(len(polygons)):
                plt.plot([v[0] for v in polygons[i]], [v[1] for v in polygons[i]], c='black')
                size = len(polygons[i])
                xvals = [polygons[i][0][0], polygons[i][size-1][0]]
                yvals = [polygons[i][0][1], polygons[i][size-1][1]]
                plt.plot(xvals, yvals, c='black') ## in order to print a closed polygon
        plt.show()

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

def GetRelevantContours(edges):
        ## returns all the contours in following order: 
        ## outermost, inner contours
        _,contours,_ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted(contours, key=cv2.contourArea, reverse=True)
        ## contours[4] -- outer
        ## contours[5] -- inner
        cnt4 = contours[4]
        cnt5 = contours[5]
        print(cnt4)
        return cnt4, cnt5

def DisectPolygons(path, blocked):
        pc = pyc.Pyclipper()
        pc.AddPath(path, pyc.PT_SUBJECT, True)
        pc.AddPath(blocked, pyc.PT_CLIP, True)
        return pc.Execute(pyc.CT_DIFFERENCE)

def DisplayImage(text, img):
        ## Diplay image
        cv2.imshow(text, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def GetHoleCenterpoints(cnt):
        M = cv2.moments(cnt)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
        return cX, cY
        
def CreateNavMesh(pathToPic):
        edged = ProcessImage(pathToPic)
        cnts = GetRelevantContours(edged) 

        outer = cnts[0]
        inner = cnts[1]
        print("len(cnts): ", len(cnts) )
        # cv2.drawContours(edged, [outer], -1, (150,0,0), 3)
        # block = cv2.convexHull(inner, False) ## Note assuming only ONE CONTOUR INSIDE; also: Counter-clockwise order
        # cv2.drawContours(edged, [block], -1, (150, 0, 0), 3) ## Good enough

        # total = []
        # path = []
        # for i in range(len(outer)):
        #         path.append((int(outer[i][0][0]), int(outer[i][0][1])))
        #         total.append((int(outer[i][0][0]), int(outer[i][0][1])))

        # blocked = []
        # for i in range(len(block)): ## what if there's more than one inner contour?
        #         blocked.append((int(block[i][0][0]), int(block[i][0][1])))
        #         total.append((int(block[i][0][0]), int(block[i][0][1])))


        # # tri = tr.Triangulation(pathx, pathy)
        # # print(tri.triangles.shape[0])
        # # mask_init = np.zeros()
        # # triangles.set_mask()

        # result = DisectPolygons(path, blocked)
        # DrawImage(result)
        # print(result)

        # # result = np.array(result)
        # tri = Delaunay(result)
        # plt.triplot(result[:,0], result[:,1], tri.simplices.copy())
        # plt.plot(result[:,0], result[:,1], 'o')
        # plt.scatter([v[0] for v in result], [v[1] for v in result], c='black')
        # plt.show()
        # print(result[0])
        
        # segments = tr.convex_hull(path)
        # vertices = np.array(blocked)

        # plt.scatter([v[0] for v in total], [v[1] for v in total], c='black')
        # plt.show()

        v = []
        vm = []
        s = []
        sm = []
        ctr = 1

        if len(cnts) > 1: ## atleast one inner contour
                blk = cnts[1:]

        print("len(o), len(1)", len(cnts[0]), len(cnts[1]))

        for cnt in cnts:
                ## add to vertex, vertex marker = ctr
                for i in range(len(cnt)):
                        v.append((int(cnt[i][0][0]), int(cnt[i][0][1])))
                        vm.append([ctr])
                j = 0
                while j in range(len(cnt) - 1):        
                        s.append([j, j+1])
                        sm.append([ctr])
                        j = j+1
                
                s.append([j, j-(len(cnt)-1)])
                sm.append([ctr])
                ctr = ctr+1
        
        holes = []
        for cnt in blk:
                [x, y] = GetHoleCenterpoints(cnt)
                holes.append([x, y])

        A = {'vertices':np.array(v), 'segments': np.array(s), 'segment_markers': np.array(sm), 
                'vertex_markers': np.array(vm), 'holes': np.array(holes)}
        # A = {'vertices':np.array(v), 'segments': np.array(s), 'segment_markers': np.array(sm), 
        #         'vertex_markers': np.array(vm)}

        B = tr.triangulate(A, 'p')
        # print(A)
        tr.plot(plt.axes(), **B)
        plt.show()

        # DisplayImage('Canny', edged)

if __name__ == "__main__":
        CreateNavMesh("data/pic_nolabel.jpg")