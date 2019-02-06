from PictureProcessing import pp_module as pp
from PathFinding import pf_module as pf

if __name__ == "__main__":
        tVertInd = pp.CreateNavMesh("data/pic_nolabel.jpg")
        tIds = pp.GetTriangles(tVertInd)

        s,e = pf.FindStartEndTri(tIds, (174,56), (1342,552))
        path = pf.FindPath(tIds, s, e)
