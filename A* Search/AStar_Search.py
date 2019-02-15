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
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])

        return dx + dy

    def get_vertex_neighbours(self, pos):
        n = []
        #Moves allow link a chess king
        # for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
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
                raise RuntimeError("A* Blocked Path!")
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
    # Load the image & resize
    img_large = cv2.imread('data/pic.JPG',0)
    img = cv2.resize(img_large, (0,0), fx=0.25, fy=0.25)

    # Blur the image and convert to array
    blurred = cv2.GaussianBlur(img,(5,5),0)
    laplacian = cv2.Canny(blurred, 50, 200, 255)
    num_rows = len(laplacian)
    num_columns = len(laplacian[0])
    
    # create a graph with the required columns and rows
    graph = AStarGraph(num_columns, num_rows)

    # filter the array to limit to 1s and 0s
    # Add all zero indexes to barriers list in graph
    for i in range(num_rows):
        for j in range(num_columns):
            if laplacian[i][j] <= 10:
                laplacian[i][j] = 1
            else:
                laplacian[i][j] = 0
                graph.addBarrier(i,j)

    # # Get user input 
    # start = raw_input("Enter starting room: ")
    # dest = raw_input("Enter destination room: ")

    # # initial hard code for room locations
    # rooms = {
    #     "A" : [26, 11],
    #     "B" : [26, 56],
    #     "C" : [48, 11],
    #     "D" : [47, 56]
    # }

    # # Assume the input from user is valid (Room is A, B, C or D)
    # src_x = rooms[start][0]
    # src_y = rooms[start][1]
    # dest_x = rooms[dest][0]
    # dest_y = rooms[dest][1]
    # src_z = np.sqrt(src_x**2 + src_y**2)
    # verts = np.array([[-1, -1], [1, -1], [1, 1], [-1, -1]])

    # # Send the location, destination and graph to A*
    # result, cost = AStarSearch((src_x,src_y), (dest_x,dest_y), graph)
    # print ("route", result)
    # print ("cost", cost)

    # # Plot the final result
    # plt.plot([v[0] for v in result], [v[1] for v in result], 'r-', linewidth=3.0)
    # plt.scatter(src_x, src_y, s=80, c=src_z, marker=(12, 0))
    # plt.scatter(dest_x, dest_y, s=100, c=src_z, marker='D')
    for barrier in graph.barriers:
        plt.scatter([v[0] for v in barrier], [v[1] for v in barrier], c='black')

    plt.xlim(0,num_rows)
    plt.ylim(0,num_columns)
    plt.show()