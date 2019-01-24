import cv2
import matplotlib.pyplot as plt
import numpy as np
import triangle as tr
import pp_getcontours as pp

def GetHoleCenterpoints(cnt):
        M = cv2.moments(cnt)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
        return cX, cY
        
def CreateNavMesh(pathToPic):
        edged = pp.ProcessImage(pathToPic)
        cnts = pp.GetRelevantContours(edged) 

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
                [x, y] = GetHoleCenterpoints(cnt)
                holes.append([x, y])

        A = {'vertices':np.array(v), 'segments': np.array(s), 'segment_markers': np.array(sm), 
                'vertex_markers': np.array(vm), 'holes': np.array(holes)}

        B = tr.triangulate(A, 'p')
        tr.plot(plt.axes(), **B)
        plt.show()

if __name__ == "__main__":
        CreateNavMesh("data/pic_nolabel.jpg")