from distutils.command.config import config
from p5 import Vector, random_uniform
from .ScreenObject import ScreenObject
from app.config import data as c
import logging
from concurrent.futures import ThreadPoolExecutor as Executor

class MovingObject(ScreenObject):
    
    def __init__(self, vXY, width, height, vVelocity) -> None:
        super().__init__(vXY, width, height)
        # self.velocity = vVelocity
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)
        self.mass = float(0)
        # self.velocity = Vector.random_2D()
        # self.velocity = self.velocity * random_uniform(vVelocity.x, vVelocity.y)
    
        
    def applyForce(self, force):
        f = force / self.mass
        self.acceleration = self.acceleration + f
       
    
    def attract(self):
        pass
     
    def sendForceToNeighbours(self):
        for entity in self.quadTree.entities:
            entity.applyForce(self.mass)

    def move(self):
        # self.sendForceToNeighbours()
        self.velocity = self.velocity + self.acceleration
        self.pos = self.pos + self.velocity
        self.contain()
        isElementInSquare = self.quadTree.checkElementInSquare(self)
        self.acceleration = Vector(0,0)
        
        if (not isElementInSquare):
            tempQuadTree = self.quadTree
            # find new square. self.quadtree automatically gets updated by doing 'add'
            
            self.quadTree.head.add(self)    
            tempQuadTree.removeEntity(self)
            tempQuadTree.desplitCheck()
            logging.debug(f"\n\n Element no longer in square {self.pos.x} {self.pos.y}")
    
    def contain(self):
        if self.pos.x >= c["canvasWidth"] - self.widthOffset:
            self.pos.x = c["canvasWidth"] - self.widthOffset
            self.velocity.x *= -1
        elif self.pos.x <= 0 + self.widthOffset:
            self.pos.x = 0 + self.widthOffset
            self.velocity.x *= -1
        
        if self.pos.y > c["canvasHeight"] - self.heightOffset:
            self.pos.y = c["canvasHeight"] - self.heightOffset
            self.velocity.y *= -1
        elif self.pos.y < 0 + self.heightOffset:
            self.pos.y = 0 + self.heightOffset
            self.velocity.y *= -1