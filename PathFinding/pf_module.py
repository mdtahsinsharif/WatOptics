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

    if abs(dx) <= abs(dy): ## in the case where dx = dy, we are forcing x movement first.
        # grad = 10
        grad = 1
    else: ## dx > dy
        # grad = abs(dy)/abs(dx)
        grad = 0

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
    segments.append(1)
    direction_prev = []
    
    prevp = tIds[path[1]].GetMidpoint()
    currentp = tIds[path[2]].GetMidpoint()

    grad_prev = gradient(prevp, currentp)[0]

    i = 2
    while i < len(path)-1:
        nextp = tIds[path[i+1]].GetMidpoint()
        grad_new = gradient(currentp, nextp)[0]
        
        if grad_new != grad_prev:
            segments.append(i)
            direction_prev.append(grad_prev) ## before this point, we were moving in grad_prev direction
        
        currentp = nextp
        grad_prev = grad_new
        i += 1
    
    segments.append(i) ## i = len(path) - 1 
    direction_prev.append(grad_prev)
    print("segments: ", segments)
    return segments, direction_prev

def Optimizer(tIds, path, start, dest):
    '''
    With the initial list of ids which are potentially involved in this path,
    this function will come up with a final list of coordinates to visit.
    '''

    ## Issues with rooms: 4032-4036
    ## 4116 - 4112
    ## 4017 - 4116

    newpath = []
    newpath.append(start)
    if len(path) <= 1: ## TODO: This should be 2, and we need to digitize
        # both the start and dest are in the same triangle
        newpath.append(dest)
        return newpath

    segments, direction = getSegments(tIds, path, start, dest)    
    # print(path)
    # print(segments)

    avg_points = []

    for i in range(len(segments)-1):
        segmented_path = path[segments[i]:segments[i+1]+1] ## if segments from 0 to 5, we want index 5 included 
        length = len(segmented_path)

        sum_x = 0
        sum_y = 0

        for id in segmented_path:
            point = tIds[id].GetMidpoint()
            print("p ", point)
            sum_x += point[0]
            sum_y += point[1]

        avg_x = sum_x/length
        avg_y = sum_y/length  

        avg_points.append((avg_x, avg_y))

    print("avg ", avg_points)

    ## avg_points contains the avg of all the corridors at this point ideally. 

    ## digitize and append the start and end points 
    optPath = []

    optPath.append(start)
    current = start

    for i in range(len(avg_points)):
        d = direction[i] ## dx <= dy ---> move in y? 
        point = avg_points[i]
        print("direction ", d)
        if d: ## moving in y
            optPath.append((point[0], current[1]))
            current = (point[0], current[1])
        else: ## moving in x 
            optPath.append((current[0], point[1]))
            current = (current[0], point[1])

        # optPath.append(point)

    d = gradient(current, dest)[0]

    if d:
        optPath.append((current[0], dest[1]))
    else:
        optPath.append((dest[0], current[1]))
    
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

def getTurn(p1, p2, p3):
    '''
    https://stackoverflow.com/questions/38856588/given-three-coordinate-points-how-do-you-detect-when-the-angle-between-them-cro?rq=1
    '''
    crossproduct = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    if crossproduct == 0:
        return 'F'
    elif crossproduct > 0:
        return 'R'
    else:
        return 'L'

def getNumSteps(p1, p2, sc):
    stepsx = m.ceil(abs(p1[0] - p2[0])/sc)
    stepsy = m.ceil(abs(p1[1] - p2[1])/sc)

    if stepsx != 0:
        return stepsx
    else:
        return stepsy

def GetInstructions(path, sc): ## sc = stride scale
    ## ASSUMPTION: We start with our back to the door
    ## TODO: Global sc

    instructions = [] ## list of tuples (dir, num steps)
    
    if len(path) <= 1:
        ## no path, already at destination
        return 

    instructions.append(('F', getNumSteps(path[0], path[1], sc)))

    i = 1
    prevp = path[0]
    currentp = path[1]
    while i in range(len(path) - 1):
        nextp = path[i+1]

        direction = getTurn(np.array(prevp), np.array(currentp), np.array(nextp))
        instructions.append((direction, getNumSteps(currentp, nextp, sc)))
        currentp = nextp
        i +=1
    
    print(instructions)
    return instructions



