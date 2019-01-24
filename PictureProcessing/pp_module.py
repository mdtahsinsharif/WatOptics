import matplotlib.pyplot as plt
import numpy as np
import triangle as tr
import opencv_wrapper as cv_wpr

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

def CreateNavMesh(path):
        edged = cv_wpr.ProcessImage(path)
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
                for i in range(len(cnt)):
                        v.append((int(cnt[i][0][0]), int(cnt[i][0][1])))
                        vm.append([ctr])
                j = start_index
                while j in range(start_index + len(cnt) - 1):        
                        s.append([j, j+1])
                        sm.append([ctr])
                        j = j+1
                
                s.append([j, j-(len(cnt)-1)])
                sm.append([ctr])
                ctr = ctr+1
                start_index = len(cnt)
        
        holes = []
        for cnt in blk:
                [x, y] = cv_wpr.GetHoleCenterpoints(cnt)
                holes.append([x, y])

        A = {'vertices':np.array(v), 'segments': np.array(s), 'segment_markers': np.array(sm), 
                'vertex_markers': np.array(vm), 'holes': np.array(holes)}

        B = tr.triangulate(A, 'pD') ## prefer this or p or pq?
        tr.plot(plt.axes(), **B)
        plt.show()

        return B['triangles'].tolist()

def GetTriangles(unsorted_triangles):
        '''
        Sorts the list of triangles so each knows what neighbors it has
        returns the new list
        '''

# for debugging only
if __name__ == "__main__":
        CreateNavMesh("../data/pic_nolabel.jpg")