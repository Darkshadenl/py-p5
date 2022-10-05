from collections import namedtuple
from msilib.schema import Error
from p5 import Vector

class QuadRectangle:
    
    def __init__(self, size, zeroPoint = -1, 
                 midPoint = -1, 
                 vZeroPoint: Vector = None) -> None:
        self.size: int = size
        
        if zeroPoint != -1:
            self.zeroPoint : int = zeroPoint
        else:
            self.setupMidPointClass(midPoint, vZeroPoint)
        
    def setupMidPointClass(self, midPoint, vZeroPoint: Vector):
        if vZeroPoint == None:
            raise Error("vZeroPoint is of wrong type")
        
        Position = namedtuple('Position', ['topLeft', 'bottomRight'])
        
        midPointX2 = midPoint * 2
        tL1 = vZeroPoint
        tL2 = vZeroPoint + Vector(midPoint, midPoint)
        tR1 = vZeroPoint + Vector(midPoint, 0)
        tR2 = vZeroPoint + Vector(midPointX2, midPoint)
        bL1 = vZeroPoint + Vector(0, midPoint)
        bL2 = vZeroPoint + Vector(midPoint, midPointX2)
        bR1 = vZeroPoint + Vector(midPoint, midPoint)
        bR2 = vZeroPoint + Vector(midPointX2, midPointX2)
        
        self.positions = [
            Position(tL1, tL2),
            Position(tR1, tR2),
            Position(bL1, bL2),
            Position(bR1, bR2)
        ]        
        
    def intersectFromZeropoint(self, contender: Vector):
        tL = Vector(self.zeroPoint, self.zeroPoint)
        bR = tL + Vector(self.size, self.size)
        
        if contender <= bR and contender >= tL:
            return True
        else:
            return False
    
    
    def intersectFromMidpoint(self, contender: Vector, added):
        # return 0 - 3
        for i in range(0, len(self.positions)):
            p = self.positions[i]
            
            x: int = int(contender.x)
            y: int = int(contender.y)
            
            conditions = (
                x <= int(p.bottomRight.x),
                y <= int(p.bottomRight.y),
                x >= int(p.topLeft.x),
                y >= int(p.topLeft.y)
            )
            
            check = all(conditions)
            
            if check:
                return i
        raise Exception("Something went wrong @ intersectMidpoint")
