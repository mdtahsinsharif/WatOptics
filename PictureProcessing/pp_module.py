# import matplotlib.pyplot as plt ## for debugging CreateNavMesh
import numpy as np
import triangle as tr
import opencv_wrapper as cv_wpr
import polygon as nvs_p ## navspex polygon
import matplot_wrapper as plt_wpr
import math as m

'''
Notes:
[1] https://rufat.be/triangle/API.html
'''

'''
TODO:
[1] the list we get from contours has points very close together, it makes the triangles very small
        and ugly --> increases the number of triangles for no reason. Need to figure out how to optimize
        the contour points to avoid this. 
[2] According to: https://www.gamedev.net/articles/programming/artificial-intelligence/generating-2d-navmeshes-r3393/
        we want to have the triangles roughly equal length. triangulate with options 'pq' seems to acheive this. 
        Need to test it on different maps.
        Update: 'pD' gives better triangles
'''

def ReadImage(pathToImg):
        img = cv_wpr.ImgToNumpy(pathToImg)
        edged = cv_wpr.ProcessImage(img)
        return img, edged

def CreateNavMesh(edged):
        cnts = cv_wpr.GetRelevantContours(edged) 

        v = []
        vm = []
        s = []
        sm = []
        ctr = 1

        if len(cnts) > 1: ## atleast one inner contour
                blk = cnts[1:]

        start_index = 0
        for cnt in cnts:
                ## add to vertex, vertex marker = ctr
                # print(cnt)
                for i in range(len(cnt)):
                        print(cnt[i][0], int(cnt[i][1]))
                        v.append((int(cnt[i][0]), int(cnt[i][1])))
                        vm.append([ctr])
                j = start_index
                while j in range(start_index + len(cnt) - 1):        
                        s.append([j, j+1])
                        sm.append([ctr])
                        j = j+1
                
                s.append([j, j-(len(cnt)-1)])
                sm.append([ctr])
                ctr = ctr+1
                start_index += len(cnt)
        
        holes = []
        for cnt in blk:
                [x, y] = cv_wpr.GetHoleCenterpoints(np.array(cnt))
                holes.append([x, y])

        A = {'segment_markers': np.array(sm), 'segments': np.array(s), 'vertex_markers': np.array(vm), 
                'vertices':np.array(v), 'holes': np.array(holes)}
        B = tr.triangulate(A, 'p')
        
        # ## Only for Debugging
        # tr.plot(plt.axes(), **B)
        # plt.show()
        
        v = np.array(v)
        tList = B['triangles'].tolist()
        tCoords = [] ## coordinates of the triangles: [[[0,0], [0,1], [1,0]], [...]]
        for t in tList:
                tCoords.append([v[t[0]], v[t[1]], v[t[2]]])

        return tCoords

def AddNeighbors(t1, t2):
        '''
        Calculates the distance between the midpoints of t1 and t2
        which represent triangle 1 and triangle 2 
        And then adds each to each others neighbors
        '''
        x1, y1 = t1.GetMidpoint()
        x2, y2 = t2.GetMidpoint()
        distance = int(m.sqrt((x1-x2)**2 + (y1-y2)**2))

        t1.AddNeighbor(t2.GetId(), distance)
        t2.AddNeighbor(t1.GetId(), distance)

def GetTriangles(trilist):
        '''
        Sorts the list of triangles so each knows what neighbors it has
        returns the new list
        '''
        tIds = {} ## map --> id, triangle
        edges = {} ## map --> edge, id
        for vlist in trilist:
                tId = len(tIds) + 1
                tIds[tId] = nvs_p.triangle(tId, vlist)
                
                for i in range(len(vlist)):
                        ## add to dictionary
                        edges.setdefault(
                                "({},{})".format(vlist[i][0],vlist[i][1]), 
                                        []).append(tId)

                
                j = 0        
                while j in range(len(vlist)-1):
                        s1 = set(edges["({},{})".format(vlist[j][0], vlist[j][1])])
                        s2 = set(edges["({},{})".format(vlist[j+1][0], vlist[j+1][1])])

                        neighbors = s1 & s2 ## set intersection
                        for nId in neighbors:
                                if nId == tId:
                                        continue
                                AddNeighbors(tIds[nId], tIds[tId])
                        j = j+1
                
                x0 = vlist[0][0]
                y0 = vlist[0][1]
                xN = vlist[j][0]
                yN = vlist[j][1]

                ## add to dictionary
                edges.setdefault(
                        "({},{})".format(xN,yN), 
                                []).append(tId)
                
                s1 = set(edges["({},{})".format(xN, yN)])
                s2 = set(edges["({},{})".format(x0, y0)])

                neighbors = s1 & s2 ## set intersection
                for nId in neighbors:
                        if nId == tId:
                                continue
                        AddNeighbors(tIds[nId], tIds[tId])
        
        return tIds

## for debugging only
# if __name__ == "__main__":
#         img, edged = ReadImage("../data/e5_4f_nolabel.jpg")
#         tVertInd = CreateNavMesh(edged)
#         tIds = GetTriangles(tVertInd)
#         plt_wpr.DrawNeighbors(tIds, 5)
#         plt_wpr.ShowPlot()