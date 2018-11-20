from __future__ import print_function
import matplotlib.pyplot as plt
import cv2
import numpy as np

class AStarGraph(object):
    #Define a class board like grid with two barriers
    global blockCost
    blockCost = 10000
    def __init__(self, r, c):
        self.barriers = []
        self.barriers.append([])
        self.gridCol = c
        self.gridRows = r
        # self.barriers.append([(2,1),(1,1),(2,4),(2,5),(2,6),(3,6),(4,6),(5,6),(5,5),(5,4),(5,3),(5,2),(4,2),(10,6)])
    
    def addBarrier(self,x, y):
        self.barriers[0].append((x,y))
        
    def getBarrier(self,x,y):
        return self.barriers;
    
    def heuristic(self, start, goal):
        #Use Chebyshev distance heuristic if we can move one square either
        #adjacent or diagonal
        D = 1
        D2 = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
        
    def get_vertex_neighbours(self, pos):
        n = []
        #Moves allow link a chess king
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 < 0 or x2 > self.gridCol or y2 < 0 or y2 > self.gridRows:
                continue
            n.append((x2, y2))
        return n

    def move_cost(self, a, b):
        for barrier in self.barriers:
            if b in barrier:
                return blockCost #Extremely high cost to enter barrier squares
        return 1 #Normal movement cost

def AStarSearch(start, end, graph):

    G = {} #Actual movement cost to each position from the start position
    F = {} #Estimated movement cost of start to end going via this position

    #Initialize starting values
    G[start] = 0 
    F[start] = graph.heuristic(start, end)

    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        #Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        #Check if we have reached the goal
        if current == end:
            #Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            if F[end] >= blockCost:
                raise RuntimeError("A* failed to find a solution")
            return path, F[end] #Done!

        #Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        #Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closedVertices: 
                continue #We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)

            if neighbour not in openVertices:
                openVertices.add(neighbour) #Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue #This G score is worse than previously found

            #Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")

if __name__=="__main__":
    # graph = AStarGraph(10, 10)
    # graph.addBarrier(4,3)
    # graph.addBarrier(7,6)
    # graph.addBarrier(6,6)
###############    
    img = cv2.imread('tiny_img.jpg',0)
    # print(img)
    # img2 = cv2.imread('dc_3rd.JPG',150)

    blurred = cv2.GaussianBlur(img,(5,5),0)
    laplacian = cv2.Laplacian(blurred,cv2.CV_64F)

    # newlaplacian = laplacian
    num_rows = len(laplacian)
    num_columns = len(laplacian[0])
    graph = AStarGraph(num_rows, num_columns)
    for i in range(num_rows):
        for j in range(num_columns):
            if laplacian[i][j] <= 5: #found this number by trial and error, need to find a way to do this for all maps
                # newlaplacian[i][j] = 1
                laplacian[i][j] = 1
            else:
                # newlaplacian[i][j] = 0
                laplacian[i][j] = 0
                graph.addBarrier(i,j)

#################

    result, cost = AStarSearch((0,0), (10,5), graph)
    print ("route", result)
    print ("cost", cost)
    # print(graph.barriers)
    plt.plot([v[0] for v in result], [v[1] for v in result])
    for barrier in graph.barriers:
        plt.scatter([v[0] for v in barrier], [v[1] for v in barrier])
    plt.xlim(-1,num_columns)
    plt.ylim(-1,num_rows)
    plt.show()