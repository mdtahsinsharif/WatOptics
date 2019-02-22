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
    dy/dx of line from p1 to p2
    '''
 
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    if abs(dx) < abs(dy):
        grad = 10
    else:
        grad = abs(dy)/abs(dx)

    return grad, dx, dy
    

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


def FindPolygonsInPath(tIds, current, dest):
    '''
    Inputs:
    current: coordinates of the current location of the user
    dest: coordinates of the destination
    tIds: dictionary; maps triangle Ids to actual triangles
    
    Output:
    returns a list containing the ids of the triangles which form the fastest path
    from the start to the end
    '''

    start, end = FindStartEndPoly(tIds, current, dest)

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

            # for node in path: 
            #     print(node, G[node])
            
            # print(end, G[end])
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

            G[nId] = costToNeighbor
            cameFrom[nId] = current
            F[nId] = G[nId] + Heuristic(tIds[nId].GetMidpoint(), tIds[end].GetMidpoint())
            
    raise RuntimeError("Algorithm failed to find a solution")

def getSegments(tIds, path, start, end):
    segments = []
    segments.append(0)
    
    current = tIds[path[0]].GetMidpoint()
    grad_old, dx, dy = gradient(start, current)

    direction = []
    direction.append(grad_old)

    i = 1
    while i < len(path):
        next_m = tIds[path[i]].GetMidpoint()

        grad_new, dx, dy = gradient(current, next_m)

        print(i, dx, dy, grad_new)
        
        if ((grad_new/4 >= grad_old) or (grad_old/4 >= grad_new)) and not (grad_new == grad_old): ## chosen factor of 10
            ## and not (grad_new ==0 and grad_old==0)
            ## Note: if grad_new and grad_old are both 0, the first conditions are always met. 
            segments.append(i)
            direction.append(grad_new)

        current = next_m
        grad_old = grad_new
        i += 1

    # if segments[len(segments)-1] != path[len(path)-1]:
    #     # segments.append(path[len(path)-1])
    #     direction.append(gradient(current, end)[0])
    
    return segments, direction

def Optimizer(tIds, path, start, dest):
    '''
    With the initial list of ids which are potentially involved in this path,
    this function will come up with a final list of coordinates to visit.
    '''

    newpath = []
    newpath.append(start)
    if len(path) == 1:
        # both the start and dest are in the same triangle
        newpath.append(dest)
        return newpath

    segments, direction = getSegments(tIds, path, start, dest)    
    print(path)
    print(segments)

    ## for debugging
    # seg_coords = []
    # for i in range(len(segments)):
    #     seg_coords.append(tIds[path[i]].GetMidpoint())
    
    # print(seg_coords)

    ## for each segment, find the avg_x and avg_y values
    ## 0 - start to 0
    ## 1 - 0 to 1 and so on

    avg_coords = []
    avg_coords.append((start[0], start[1], direction[0])) ## -1 indicates we're not sure which {x or y} is constant

    for j in range(len(segments)-1):
        segmented_path = path[segments[j]:segments[j+1]]
        print(segmented_path)
        length = len(segmented_path)

        sum_x = 0
        sum_y = 0

        for id in segmented_path:
            point = tIds[id].GetMidpoint()
            sum_x += point[0]
            sum_y += point[1]

        avg_x = sum_x/length
        avg_y = sum_y/length

        ## if dx_local >= dy_local, change in x is greater and y will be constant
        ## therefore, x, y, 1 {indicating y is constant}
        ## otherwise x, y, 0 {indicating x is constant}
        avg_coords.append((avg_x, avg_y, direction[j]))

    avg_coords.append((dest[0], dest[1], direction[len(direction)-1]))

    optPath = []
    optPath.append(start)
    for i in range(len(avg_coords)-1):
        print(avg_coords[i][2])
        # optPath.append((avg_coords[i][0],avg_coords[i][1]))
        current = avg_coords[i]
        nextc = avg_coords[i+1]
        # print(current)
        if current[2] > 0:
            ## x must stay constant
            ## end point here will be: (current(x), next(y))
            optPath.append((current[0], nextc[1]))
        else:  
            optPath.append((nextc[0], current[1]))

    optPath.append(dest)

    print("optPath: ", optPath)

    return optPath

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
    path, dist = FindPolygonsInPath(tIds, current, dest)
    coordinates = Optimizer(tIds, path, current, dest)
    return coordinates, path, dist



