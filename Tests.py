from PictureProcessing import pp_module as pp
from PictureProcessing import matplot_wrapper as plt
from PathFinding import pf_module as pf

def DebugPathFinding():
    tVertInd = pp.CreateNavMesh("data/pic_nolabel.jpg")
    tIds = pp.GetTriangles(tVertInd)

    coords, path, dist = pf.FindPath(tIds, (174,56), (1342,552))

    print(coords)

    shortPath = pf.Optimize(coords)

    plt.DrawTriangles(tIds, path, 'hide')
    plt.ScatterPoints(shortPath, 'purple')
    plt.ShowPlot()


DebugPathFinding()