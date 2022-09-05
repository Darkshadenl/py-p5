from p5 import Vector

class ScreenObject:
    
    def __init__(self, vXY, width, height):
        self.width = width
        self.height = height
        self.widthOffset = width / 2
        self.heightOffset = height / 2
        self.pos = vXY
        self.quadTree = None
        
    def setQuadTree(self, quadTree):
        self.quadTree = quadTree
        
    def getNeighbours(self):
        qEnts = self.quadTree.entities
        return qEnts