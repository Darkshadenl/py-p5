from p5 import Vector

# Particle?
class QuadElt:
    def __init__(self, id: int, tL: Vector, bR:Vector):
        # particle id
        self.id = id
        
        # leave temp. My stuff has no size. 
        self.tL = tL
        self.bR = bR