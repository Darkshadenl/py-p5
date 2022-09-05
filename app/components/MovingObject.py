from p5 import Vector, random_uniform
from .ScreenObject import ScreenObject
from app.config import data as c

class MovingObject(ScreenObject):
    
    def __init__(self, vXY, width, height, vVelocity) -> None:
        super().__init__(vXY, width, height)
        self.velocity = vVelocity
        self.velocity = Vector.random_2D()
        self.velocity = self.velocity * random_uniform(vVelocity.x, vVelocity.y)

    def move(self):
        self.pos = self.pos + self.velocity
        self.contain()
        self.quadTree.desplitCheck()
    

    def contain(self):
        if self.pos.x > c["canvasWidth"] - self.widthOffset or self.pos.x < 0 + self.widthOffset: 
            self.velocity.x = -self.velocity.x
        
        if self.pos.y > c["canvasHeight"] - self.heightOffset or self.pos.y < 0 + self.heightOffset:
            self.velocity.y = -self.velocity.y
        