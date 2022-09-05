from p5 import *

class ParticleBorder:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self):
        line(self.p1.pos.x, self.p1.pos.y, self.p2.pos.x, self.p2.pos.y)
        stroke("blue")
        stroke_weight(2)