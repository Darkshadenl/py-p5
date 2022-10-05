import logging
from app.dataStructures.QTree import QTree

from app.dataStructures.QuadTree import QuadTree
from p5 import Vector,  random_uniform
from app.components.Particle import Particle
from app.config import data as c
from app.helpers.ElementTracker import tracker as undotracker
from app.helpers.ActiveSquaresTracker import squareTracker

class MainModel:
    
    def __init__(self, width, height, numberOfEntities):
        self.undoTracker = undotracker
        self.entities = []
        self.numberOfEntities = numberOfEntities
        self.logger = logging.getLogger()
        self.width = width
        self.height = height
        self.quadTree = QuadTree(Vector(width, height), Vector(0,0), tag='base')
        self.quadTree.head = self.quadTree
        self.undoTracker.add(self.quadTree)
        self.activeSquaresTracker = squareTracker
        self.QTree = QTree(c["canvasWidth"])
        
    
    def addEntity(self, Particle):
        self.undoTracker.add(self.quadTree)
        self.quadTree.add(Particle)
        
    def undo(self):
        o = self.undoTracker.undo(self.quadTree)
        self.quadTree = o
    
    def redo(self):
        o = self.undoTracker.redo()
        if o is not None:
            self.quadTree = o
    
    def setup(self):
        for index in range(self.numberOfEntities):
            vXY = self.setupPosition()
            velocity = self.setupVelocity()
            particle = Particle(vXY, velocity)
            self.entities.append(particle)
            self.quadTree.add(particle)
            self.QTree.add(particle)
        
    def setupVelocity(self):
        noVelocity = c["noVelocity"]
        
        if noVelocity == False:
            self.logger.info("Config velocity")
            return Vector(random_uniform(c["velocityMin"], c["velocityMax"]),  
                          random_uniform(c["velocityMin"], c["velocityMax"]))
        else:
            self.logger.info("No velocity")
            return Vector(0,  0)
    
    def setupPosition(self):
        randomPosition = c["randomPosition"]
        
        if randomPosition == True:
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

    def compare(self, v1, v2):
        if v1 == v2:
            return 0
        if v1 < v2:
            return -1
        if v1 > v2:
            return 1