class Graph:
    def __init__(self):
        self.dict = {}
    
    def addVertex(self,value):
        if self.dict.has_key(value):        
            print "Vertex already exists"
        else:
            self.dict[value] = None

    def addEdge(self,value1,value2,weight):
        if self.dict.has_key(value1) and self.dict.has_key(value2):
            if self.dict[value1] == None:
                self.dict[value1] = {}
                self.dict[value1][value2] = weight
            else:
                self.dict[value1][value2] = weight
        else:
            print "One or more vertices not found."

    def findVertex(self,value):
        if self.dict.has_key(value):
            print "%d has adjacent vertices %s" % (value, str(self.dict[value]))
        else:
            print "Vertex does not exist"

    def getWeight(self,value1,value2):
        return self.dict[value1][value2]

    def getAllWeights(self,value1):
        return self.dict[value1]
