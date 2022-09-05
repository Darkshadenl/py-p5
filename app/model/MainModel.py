import logging

from app.dataStructures.QuadTree import QuadTree
from p5 import Vector,  random_uniform
from app.components.Particle import Particle
from app.config import data as c

class MainModel:
    
    def __init__(self, width, height, numberOfEntities) -> None:
        self.entities = []
        self.numberOfEntities = numberOfEntities
        self.logger = logging.getLogger()
        self.width = width
        self.height = height
        self.quadtree = QuadTree(Vector(width, height), Vector(0,0), tag='base')
    
    def setup(self):
        for index in range(self.numberOfEntities):
            vXY = self.setupPosition()
            velocity = self.setupVelocity()
            particle = Particle(vXY, velocity)
            self.entities.append(particle)
            self.quadtree.add(particle)
        
    def setupVelocity(self):
        configVelocity = c["noVelocity"]
        
        if (configVelocity == False):
            self.logger.info("Random velocity")
            return Vector(random_uniform(-1.5, 2.1),  random_uniform(-1.5, 1.5))
        else:
            self.logger.info("Config velocity")
            return Vector(random_uniform(c["velocityMin"], c["velocityMax"]),  
                          random_uniform(c["velocityMin"], c["velocityMax"]))
    
    def setupPosition(self):
        configPosition = c["noPosition"]
        
        if (configPosition == False):
            self.logger.info("Random position")
            return Vector(random_uniform(0.1, c["canvasWidth"] - 1),  random_uniform(0.1, c["canvasHeight"] - 1))
        else:
            self.logger.info("Config position")
            return Vector(random_uniform(c["xMin"], c["xMax"]),  
                          random_uniform(c["xMin"], c["xMax"]))
    
    def getEntityNeighbours(self):
        ents = []
        for e in self.entities:
            ents.extend(e)
        return ents
        