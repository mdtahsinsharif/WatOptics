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

    alphaToInd = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5
    }

    rooms = {
        "4029" : [(46, 116)],
        "4032": [(104, 116)],
        "4033": [(164, 116)],
        "4906": [(301, 116)],
        "StaircaseUP": [(1110, 448),(343, 20),  (913, 20), (1512, 20), (1005, 448)],
        "StaircaseDN": [(1110, 448),(343, 20),  (913, 20), (1512, 20), (1005, 140)],
        "E7Entrance": [(356,18), (987, 18),  (1525, 18)],
        "4037": [(426, 116)],
        "4041": [(542, 116)],
        "4043": [(661, 116)],
        "4046": [(688, 116)],
        "4048": [(729, 116)], 
        "4049": [(862, 116)],
        "4102": [(1143, 116)],
        "4103": [(1201, 116)],
        "4104": [(1227, 116)],
        "4133": [(1422, 116)],
        "4904": [(1480, 116)], 
        "4109": [(1592, 116)], 
        "4111": [(1653, 116)],
        
        "4031": [(72, 140)],
        "4036": [(186, 140), (266, 140)],
        "4028": [(72, 448)],
        "4021": [(186, 448), (266, 448)],
        
        "4038": [(429, 140)], 
        "4039": [(518, 140)],
        "4042": [(637, 140)],
        "4044": [(688, 140)],
        "4047": [(779, 140)],
        "4017": [(429, 448)],
        "4014": [(518, 448)], 
        "4011": [(604, 448)], 
        "4008": [(688, 448)],
        "4004": [(775, 448)],
        "4001": [(862, 448)], 

        "Elevator": [(1091, 183), (1091, 247)], 
        "BathroomM": [(1091, 324)], # turn left
        "BathroomF": [(1091, 324)], # turn right
        "WaterFountain": [(1091, 324)], # straight infront
        "4903": [(1180, 140)],
        "4106": [(1269, 140)], 
        "4108": [(1523, 140)], 
        "4128": [(1270, 448)],
        "4121": [(1440, 448), (1523, 448)],
        
        "4112": [(1596, 166)], 
        "4113": [(1596, 237)],
        "4114": [(1596, 351)],
        "4116": [(1596, 424)],

        "4027": [(90, 467)], 
        "4026": [(147, 467)],
        "4023": [(203, 467)],
        "4022": [(262, 467)],
        "4020": [(320, 467)],

        "4018": [(432, 467)],
        "4016": [(489, 467)],
        "4013": [(545, 467)],
        "4012": [(602, 467)],
        "4009": [(660, 467)], 
        "4007": [(718, 467)],
        "4006": [(773, 467)],
        "4003": [(832, 467)],
        "4002": [(857, 467)],
        "RoofGarden": [(943, 467)],
        "4132": [(1145, 467)],
        "4131": [(1200, 467)],
        "4129": [(1257, 467)],
        "4127": [(1316, 467)],
        "4126": [(1372, 467)], 
        "4124": [(1430, 467)],
        
        "4122": [(1486, 467)],
        "4119": [(1542, 467)],
        "4118": [(1593, 467)],
        "4117": [(1654, 467)],
    }
    ## pic_nolabel.jpg
    ## (185,77), (1231,620)
    ## simple.jpg 
    ## (18,16), (69,82)
    ## e5_4f_nolabel.jpg
    ## (36, 116), (1581, 458)
    
    ## Get user input 
    s = raw_input("Enter starting room: ")
    s = s.split(" ")
    e = raw_input("Enter destination room: ")

    # start = (36, 116)
    # end = (1581, 458)
    if len(s) > 1: 
        start = rooms[s[0]][alphaToInd[s[1]]]
    else:
        start = rooms[s[0]][0]

    ## TODO: add code to allow specific selection of destiantion staircases
    end = rooms[e]

    mindist = 10000
    for i in range(len(end)):
        # print("start: ", start)
        # print("dest: ", end[i])
        coords1, path1, dist = pf.FindPath(tIds, start, end[i])
        if dist < mindist:
            endcoords = end[i]
            coords = coords1
            path = path1
            mindist = dist
        # print("dist: ", dist)

    # print(coords)

    imgLines = wo_cv2.DrawLines(coords, img_label.copy(), 3)
    imgFinal = wo_cv2.DrawCircles((start, endcoords), imgLines, 3)
    wo_cv2.DisplayImage('Final image', imgFinal)    
    # wo_plt.DrawTriangles(tIds, path, 'hide')
    # wo_plt.ScatterPoints(coords, 'purple')
    # wo_plt.ShowPlot()

DebugPathFinding()