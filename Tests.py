from PictureProcessing import pp_module as pp
from PictureProcessing import opencv_wrapper as wo_cv2
from PictureProcessing import matplot_wrapper as wo_plt
from PathFinding import pf_module as pf
import numpy as np
import matplotlib.pyplot as plt

def DebugPathFinding():
    img_label, _ = pp.ReadImage("data/e5_4f_cutout.jpg")
    img, edged = pp.ReadImage("data/e5_4f_nolabel.jpg")
    tVertInd = pp.CreateNavMesh(edged)
    tIds = pp.GetTriangles(tVertInd)

    '''
    Hardcoding the rooms for pic.JPG for demo purposes
    '''
    # rooms = {
    #     "4038" : (185, 69),
    #     "4039": (349, 69),
    #     "4042": (564, 69),
    #     "4044": (656, 69),
    #     "4047": (819, 69),
    #     "4017": (185, 624),
    #     "4014": (347, 624),
    #     "4011": (502, 624),
    #     "4008": (646, 624),
    #     "4004": (809, 624),
    #     "4001": (969, 624),
    #     "Staircase": (1231, 624)
    # }


    ## Points for pic_nolabel.jpg
    ## (185,77), (1231,620)
    ## simple.jpg: (18,16), (69,82)
    ## Points for e5_4f_nolabel.jpg
    ## (36, 116), (1581, 458)
    
    ## Get user input 
    # s = raw_input("Enter starting room: ")
    # e = raw_input("Enter destination room: ")

    start = (36, 116)
    end = (1581, 458)
    # start = rooms[s]
    # end = rooms[e]
    coords, path, dist = pf.FindPath(tIds, start, end)

    print(coords)

    # shortPath = pf.Optimize(coords)
    imgLines = wo_cv2.DrawLines(coords, img_label.copy(), 3)
    imgFinal = wo_cv2.DrawCircles((start, end), imgLines, 3)
    wo_cv2.DisplayImage('Final image', imgFinal)    
    # wo_plt.DrawTriangles(tIds, path, 'hide')
    # wo_plt.ScatterPoints(coords, 'purple')
    # wo_plt.ShowPlot()

DebugPathFinding()