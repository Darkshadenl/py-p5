from collections import namedtuple
from msilib.schema import Error
from p5 import Vector


nodeData = namedtuple('nodeData', ['selfIndex', 'nodeIndex'])
rectangleData = namedtuple('rectangle', ['tl', 'tr'])

class Rectangle:
    
    def __init__(self, zeroPoint: Vector, width) -> None:
        self.halfWidth = width / 2
        
        self.topLeft = zeroPoint
        self.topRight = zeroPoint + Vector(width, 0)
        self.bottomLeft = zeroPoint + Vector(0, width)
        self.bottomRight = zeroPoint + Vector(width, width)
        self.middlePoint = zeroPoint + Vector(self.halfWidth, self.halfWidth)

    def isWithin(self, contender: Vector):
        if contender >= self.topLeft and contender <= self.bottomRight:
            return True
        return False
    
    def getContainerPosition(self, contender: Vector):
        """
        Purpose: gets tl, tr, bl, br for contender. 
        """
        checks = (self.withinTopLeft, self.withinTopRight, self.withinBottomLeft, self.withinBottomRight)
        results = []
        for check in checks:
            results.append(check(contender))
            
        for result in results:
            if result != -1:
                return result
        
        # all results -1
        raise Error('No valid container rectangle found')
    
    def withinTopLeft(self, contender: Vector):
        tl, br = self.getTopLeft()
        if contender >= tl and contender <= br:
            return 0
        return -1
    
    def withinTopRight(self, contender: Vector):
        tl, br = self.getTopRight()
        if contender >= tl and contender <= br:
            return 1
        return -1
    
    def withinBottomLeft(self, contender: Vector):
        tl, br = self.getBottomLeft()
        if contender >= tl and contender <= br:
            return 2
        return -1
    
    def withinBottomRight(self, contender: Vector):
        tl, br = self.getBottomRight()
        if contender >= tl and contender <= br:
            return 3
        return -1
        
        
    def getTopLeft(self):
        tl: Vector = self.topLeft
        br: Vector = self.middlePoint
        return rectangleData(tl, br)
    
    def getTopRight(self):
        tl: Vector = self.middlePoint - Vector(0, self.halfWidth)
        br: Vector = self.topRight + Vector(0, self.halfWidth)
        return rectangleData(tl, br)
    
    def getBottomLeft(self):
        tl: Vector = self.bottomLeft - Vector(0, self.halfWidth)
        br: Vector = self.middlePoint + Vector(0, self.halfWidth)
        return rectangleData(tl, br)
    
    def getBottomRight(self):
        tl: Vector = self.middlePoint
        br: Vector = self.bottomRight
        return rectangleData(tl, br)