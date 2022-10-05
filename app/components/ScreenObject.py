from p5 import Vector

from app.dataStructures.QuadTree import QuadTree

class ScreenObject:
    
    def __init__(self, vXY, width, height, id: -1):
        self.id = id
        self.width = width
        self.height = height
        self.widthOffset = width / 2
        self.heightOffset = height / 2
        self.pos = vXY
        self.quadTree = None
        
    def setQuadTree(self, quadTree):
        if isinstance(quadTree, QuadTree):
            self.quadTree = quadTree
        else:
            raise TypeError("object should be of type Quadtree")
        
    def getNeighbours(self):
        qEnts = self.quadTree.entities
        return qEnts