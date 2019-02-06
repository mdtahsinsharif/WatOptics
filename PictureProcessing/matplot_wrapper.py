import matplotlib.pyplot as plt
import polygon as p

def ShowPlot():
        plt.show()

def DrawShape(verts, clr):
        plt.plot([v[0] for v in verts], [v[1] for v in verts], 'r-', linewidth=1.0, c=clr)
        
        ## complete closed shape
        x = [verts[0][0], verts[len(verts)-1][0]]
        y = [verts[0][1], verts[len(verts)-1][1]]
        plt.plot(x, y, 'r-', linewidth=1.0, c=clr)

def MarkMidpoint(x, y, colour):
        plt.scatter(x, y, s=80, c=colour, marker=(5, 0))

def ScatterPoints(l, colour):
        plt.scatter([v[0] for v in l], [v[1] for v in l], s=80, c=colour, marker=(5,0))

def DrawNeighbors(tIds, id):
        ## Draw all triangles
        
        ## pick triangle id = id and draw in different colour
        ## draw all neighbors in a different different colour
        ## verify manually
        for i in range(len(tIds)):
                triangle = tIds[i+1]
                vertices = triangle.GetVertices()
                DrawShape(vertices, 'gray')

        triangle = tIds[id] ## manually choosing triangle
        for nId in triangle.GetNeighbors():
                neighbor = tIds[nId[0]]
                DrawShape(neighbor.GetVertices(), 'orange')
                print(nId[1])
                MarkMidpoint(neighbor.GetMidpoint()[0], neighbor.GetMidpoint()[1], 'blue')
        
        DrawShape(triangle.GetVertices(), 'red')
        MarkMidpoint(triangle.GetMidpoint()[0], triangle.GetMidpoint()[1], 'blue')

## For debugging 
def DrawTriangles(tIds, idList, keyword = 'show'):
        '''
        Draw all triangles, then draw the triangles in idList in a different colour to highlight
        '''
        for i in range(len(tIds)):
                triangle = tIds[i+1]
                vertices = triangle.GetVertices()
                DrawShape(vertices, 'gray')

        for id in idList:
                triangle = tIds[id]
                vertices = triangle.GetVertices()
                if keyword == 'show':
                        MarkMidpoint(triangle.GetMidpoint()[0], triangle.GetMidpoint()[1], 'orange')
                DrawShape(vertices, 'orange')

