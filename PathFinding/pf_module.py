from PictureProcessing import polygon as p
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import math as m
import numpy as np

def gradient(p1, p2):
    '''
    Helper funtion. 
    Inputs:
    p1: (x,y) of point 1
    p2: (x,y) of point 2

    Output: 
    dx/dy of line from p1 to p2
    '''
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    if dy == 0 :
        return 1000
    return dx/dy

def Heuristic(p1, p2):
    '''
    Inputs: 
    p1: Point 1
    p2: Point 2

    Output:
    the estimated distance between the p1 and p2
    '''

    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])
    return dx + dy


def FindStartEndPoly(tIds, current, dest):
    '''
    Inputs:
    tIds: dictionary; maps triangle Ids to actual triangle
    current: (x,y) of current user location
    dest: (x,y) of user destination

    Output:
    returns (start, end) where start is the Id of the triangle where 'current' lies
    and end is the Id of the triangle where 'dest' lies
    '''
    currentP = Point(current)
    destP = Point(dest)

    start = 0
    end = 0

    for tId in tIds:
        triangle = Polygon(tIds[tId].GetVertices())
        if start == 0 and triangle.contains(currentP):
            start = tId

        if end == 0 and triangle.contains(destP):
            end = tId

        if end != 0 and start != 0:
            break
    
    if end == 0:
        raise RuntimeError("Destination not found")
  
    if start == 0:
        raise RuntimeError("Current location not found")

    return start, end  


def FindPolygonsInPath(tIds, start, end):
    '''
    Inputs:
    start: id of the triangle where the current location of the user lies
    end: id of the triangle where the destination lies
    tIds: dictionary; maps triangle Ids to actual triangles
    
    Output:
    returns a list containing the ids of the triangles which form the fastest path
    from the start to the end
    '''

    ## cameFrom -> tId and tId
    ## G -> tId && current min value
    ## explored -> tId
    ## unexplored -> tId

    cameFrom = {}
    explored = set([])
    unexplored = set([start])
    G = {} ## actual movement cost from start to each point in graph
    F = {} ## estimated cost of movement from start to end using this position

    G[start] = 0
    F[start] = Heuristic(tIds[start].GetMidpoint(), tIds[end].GetMidpoint())

    while len(unexplored) > 0:
        ## select node with the smallest G
        current = None
        currentFCost = None
        for id in unexplored:
            if current is None or F[id] <= currentFCost:
                current = id
                currentFCost = F[current]
        
        if current == end:
            ## reached! 
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, G[end]

        ## Add to explored and remove from unexplored
        explored.add(current)
        unexplored.remove(current)

        ## analyze
        neighbors = tIds[current].GetNeighbors()
        for node in neighbors:
            nId = node[0]
            dist = node[1]

            ## if explored, do nothing
            if nId in explored:
                continue
            
            ## not in explored, add to explored
            costToNeighbor = G[current] + dist ## for A-Star, add the heuristic
            if nId not in unexplored:
                unexplored.add(nId)
            elif dist > G[nId]:
                continue ## this cost is worse, do nothing

            G[nId] = dist
            cameFrom[nId] = current
            F[nId] = G[nId] + Heuristic(tIds[nId].GetMidpoint(), tIds[end].GetMidpoint())
            
    raise RuntimeError("Algorithm failed to find a solution")

def FindPath(tIds, current, dest):
    '''
    High level function

    Inputs:
    tIds: dictionary; maps triangle Ids to actual triangle
    current: (x,y) of current user location
    dest: (x,y) of user destination

    Outputs:
    coordinates: List of (x,y) coordinates such that:
        the first point is the current
        the last point is the dest
        all other points are in order such that if followed, will lead
            user from current to dest
    path: the Ids of the triangles in the path
    dist: the total distance from current to dest using the above coordinates
    '''
    s, e = FindStartEndPoly(tIds, current, dest)
    path, dist = FindPolygonsInPath(tIds, s, e)

    coordinates = [current]
    for id in path: 
        coordinates.append(tIds[id].GetMidpoint())
    coordinates.append(dest)

    s_midpoint = tIds[path[0]].GetMidpoint()
    e_midpoint = tIds[path[len(path)-1]].GetMidpoint()

    extra_dist_s = int(m.sqrt((current[0]-s_midpoint[0])**2 + (current[1]-s_midpoint[1])**2))
    extra_dist_e = int(m.sqrt((dest[0]-e_midpoint[0])**2 + (dest[1]-e_midpoint[1])**2))
    dist += extra_dist_s + extra_dist_e

    return coordinates, path, dist

def Optimize(path):
    '''
    Inputs: 
    path: list of points in order to be visited in order to reach the dest
        the first point (x,y) is the start and the last is dest
    
    Outputs:
    newPath: shorter list of points, ideally, when connected together still
        get the user from the start to the dest without going to barriers
    '''

    newPath = [] ## start point must be there 
    dest = path[len(path)-1]

    i = 0 ## start
    while i < len(path)-2:        
        current = path[i]
        newPath.append(path[i])

        n1 = path[i+1]
        n2 = path[i+2]
        n1_dist = Heuristic(path[i+1], dest)
        n2_dist = Heuristic(path[i+2], dest)

        if n2_dist <= n1_dist:
            ## possibility of skipping n1
            ## check the gradient of the line.
            grad = abs(gradient(current, n2))
            if grad <= 0.5 or grad >= 2: ## chosen parameters
            ## dx and dy must be a factor of 2 different than
            ## each other or the line is too / 
                i = i+2
                continue
        
        i = i+1

    newPath.append(dest)

    
    # print(newPath)
    return newPath



