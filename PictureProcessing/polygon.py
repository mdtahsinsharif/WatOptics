'''
Polygon class for internal use only.
Defines class Polygon which contains:
1. TriangleID
2. Triangle Vertices List
3. Triangle Midpoint
4. Triangle Neighbors List

Note: to generalize from triangles to polygons, change the midpoint function to work for any number of vertices
'''

def midpoint(vlist):
    '''
    Note: takes a list of length 3, returns the midpoint (x,y)
    '''
    xsum = 0
    ysum = 0
    for coords in vlist:
        xsum = xsum + coords[0]
        ysum = ysum + coords[1]
    
    return (xsum/3, ysum/3)


class triangle:
    def __init__(self, id, vlist):
        self.id = id
        self.vertices = vlist
        self.midpoint = midpoint(vlist)
        self.neighbors = [] ## ids of the neighboring triangles & their distances
    
    def AddNeighbor(self, id, d):
        self.neighbors.append([id, d])

    def GetId(self):
        return self.id

    def GetMidpoint(self):
        return self.midpoint

    def GetVertices(self):
        return self.vertices
    
    def GetNeighbors(self):
        return self.neighbors

