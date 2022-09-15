from p5 import Vector, random_uniform
from .ScreenObject import ScreenObject
from app.config import data as c
import logging

class MovingObject(ScreenObject):
    
    def __init__(self, vXY, width, height, vVelocity) -> None:
        super().__init__(vXY, width, height)
        self.velocity = vVelocity
        self.velocity = Vector.random_2D()
        self.velocity = self.velocity * random_uniform(vVelocity.x, vVelocity.y)

    def move(self):
        self.pos = self.pos + self.velocity
        self.contain()
        isElementInSquare = self.quadTree.checkElementInSquare(self)
        if (not isElementInSquare):
            tempQuadTree = self.quadTree
            # find new square. self.quadtree automatically gets updated by doing 'add'
            self.quadTree.head.add(self)                        
            tempQuadTree.removeEntity(self)
            tempQuadTree.desplitCheck()
            logging.debug(f"\n\n Element no longer in square {self.pos.x} {self.pos.y}")
    
    def contain(self):
        if self.pos.x > c["canvasWidth"] - self.widthOffset or self.pos.x < 0 + self.widthOffset: 
            self.velocity.x = -self.velocity.x
        
        if self.pos.y > c["canvasHeight"] - self.heightOffset or self.pos.y < 0 + self.heightOffset:
            self.velocity.y = -self.velocity.y
        