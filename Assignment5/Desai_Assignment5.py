from Graph import Graph
import math
import sys


def fileRead(graphArray,readFile):
    o = open(readFile, 'r')
    i = 0
    for line in o:
        line = line.strip()
        j = line.split(" ")
        graphArray[i] = j
        i = i+1
    return graphArray

def addVertices(graph1, graphArray):
    rows = len(graphArray.keys())
    columns = len(graphArray[0])
    vertex = 0
    #adds vertices to graph
    for i in range (0,rows):
        for j in range (0,columns):
            graph.addVertex(vertex)
            graph1[vertex] = graphArray[i][j]
            vertex = vertex + 1
    return graph1

#adds edges to vertices in graph
def addEdges(graph,graph1):
    for i in range (0,80):
        if (i%10-1) >= 0: #node exists to left
            if int(graph1[i-1]) == 0:
                graph.addEdge(i,i-1,0)
            elif int(graph1[i-1]) == 1:
                graph.addEdge(i,i-1,-1)
            elif int(graph1[i-1]) == 2:
                graph.addEdge(i,i-1,None)
            elif int(graph1[i-1]) == 3:
                graph.addEdge(i,i-1,-2)
            else:
                graph.addEdge(i,i-1,1)

        if (i%10+1) <= 9: #node exists to right
            if int(graph1[i+1]) == 0:
                graph.addEdge(i,i+1,0)
            elif int(graph1[i+1]) == 1:
                graph.addEdge(i,i+1,-1)
            elif int(graph1[i+1]) == 2:
                graph.addEdge(i,i+1,None)
            elif int(graph1[i+1]) == 3:
                graph.addEdge(i,i+1,-2)
            elif int(graph1[i+1]) == 50:
                graph.addEdge(i,i+1,50)
            else:
                graph.addEdge(i,i+1,1)


        if i in range(0,70): #node exists below
            if int(graph1[i+10]) == 0:
                graph.addEdge(i,i+10,0)
            elif int(graph1[i+10]) == 1:
                graph.addEdge(i,i+10,-1)
            elif int(graph1[i+10]) == 2:
                graph.addEdge(i,i+10,None)
            elif int(graph1[i+10]) == 3:
                graph.addEdge(i,i+10,-2)
            else:
                graph.addEdge(i,i+10,1)


        if i in range (10,80): #node exists above
            if int(graph1[i-10]) == 0:
                graph.addEdge(i,i-10,0)
            elif int(graph1[i-10]) == 1:
                graph.addEdge(i,i-10,-1)
            elif int(graph1[i-10]) == 2:
                graph.addEdge(i,i-10,None)
            elif int(graph1[i-10]) == 3:
                graph.addEdge(i,i-10,-2)
            elif int(graph1[i-10]) == 50:
                graph.addEdge(i,i-10,50)
            else:
                graph.addEdge(i,i-10,1)



    return graph


def Reward(graph,x,y,eps):
    node = y*10 + x
    if (node%10-1) >= 0: #node exists to left
        Left = graph.getWeight(node,node-1)
    else:
        Left = None
    if (node%10+1) <= 9: #node exists to right
        Right = graph.getWeight(node,node+1)
    else:
        Right = None
    if node in range (10,80): #node exists above
        Above = graph.getWeight(node,node-10)
    else:
        Above = None
    if node in range (0,70): #node exists below
        Below = graph.getWeight(node,node+10)
    else:
        Below = None
    
    if Left != None:
        Left = Left+eps
    else:
        Left = eps
    if Right != None:
        Right = Right+eps
    else:
        Right = eps
    if Below != None:
        Below = Below+eps
    else:
        Below = eps
    if Above != None:
        Above = Above+eps
    else:
        Above = eps

    fAbove = .9*(.8*Above + .1*Left + .1*Right)
    fBelow = .9*(.8*Below + .1*Left + .1*Right)
    fLeft = .9*(.8*Left + .1*Above + .1*Below)
    fRight = .9*(.8*Right + .1*Above + .1*Below)
    if fAbove > fBelow and fAbove > fRight and fAbove > fLeft:
        if node > 10:    
            if graph.getWeight(node-10,node) != None:
                return ['up',graph.getWeight(node-10,node)+fAbove]
            else:
                return['up',fAbove]
        elif graph.getWeight(node+10,node) != None:
            return ['up',graph.getWeight(node+10,node)+fAbove]
        else:
            return['up',fAbove]
    elif fBelow > fLeft and fBelow > fRight:
        if node < 70:    
            if graph.getWeight(node+10,node) != None:
                return ['down', graph.getWeight(node+10,node)+fBelow]
            else:
                return['down',fBelow]
        elif graph.getWeight(node-10,node) != None:
            return ['down', graph.getWeight(node-10,node)+fBelow]
        else:
            return['down',fBelow]
    elif fLeft > fRight:
        if node != 50 and node != 60:
            if graph.getWeight(node-1,node) != None:
                return ['left',graph.getWeight(node-1,node)+fLeft]
            else:
                return ['left',fLeft]
        elif graph.getWeight(node+1,node) != None:
            return ['left', graph.getWeight(node+1,node)+fLeft]
        else:
            return['left',fLeft]
    else:
        if node%10 != 9:
            if graph.getWeight(node+1,node) != None:
                return ['right',graph.getWeight(node+1,node)+fRight]
            else: 
                return ['right',fRight]
        elif graph.getWeight(node-1,node) != None:
            return ['right', graph.getWeight(node-1,node)+fRight]
        else:
            return['right',fRight]
def valueIteration(graph,eps):

    oldValue = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    newValue = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
    for x in range (0,10):
        for y in range (0,8):
            oldValue[y][x] = Reward(graph,x,y,eps)
    for x in range (0,10):
        for y in range (0,8):
            delta = 10000
            while delta > eps*(1-.9)/.9:
                if oldValue[y][x][0] == 'left' and x > 0:
                    newValue[y][x] = Reward(graph,(x-1),y,eps)
                elif oldValue[y][x][0] == 'right' and x < 9: 
                    newValue[y][x] = Reward(graph,(x+1),y,eps)
                elif oldValue[y][x][0] == 'up' and y < 7:
                    newValue[y][x] = Reward(graph,x,(y+1),eps)
                elif oldValue[y][x][0] == 'down' and y > 0:
                    newValue[y][x] = Reward(graph,x,(y-1),eps)
                else:
                    newValue[y][x] = Reward(graph,x,y,eps)
                delta = oldValue[y][x][1] - newValue[y][x][1]
                oldValue[y][x] = newValue[y][x]
            
             

    oldValue[0][9] = ["stay",50]
    return oldValue

readFile = sys.argv[1]
eps = sys.argv[2]
graphArray = {}
graph1 = {}

graph = Graph()

graphArray = fileRead(graphArray,readFile)
graph1 = addVertices(graph1,graphArray)
graph = addEdges(graph,graph1)


V = valueIteration(graph,float(eps))
print "node (0,0) is bottom left, (0,1) is above that, (1,0) is to the right:"
i = 7
j = 0
for valueRow in V:
    for value in valueRow:
        print "(",j,",",i,"):",value
        j = j + 1
    i = i - 1
    j = 0


