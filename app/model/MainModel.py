from importlib.metadata import metadata
import logging

from app.dataStructures.QuadTree import QuadTree
from p5 import Vector,  random_uniform
from app.components.Particle import Particle
from app.config import data as c
from app.helpers.ElementTracker import tracker
from app.helpers.ActiveSquaresTracker import squareTracker

class MainModel:
    
    def __init__(self, width, height, numberOfEntities) -> None:
        self.elementTracker = tracker
        self.entities = []
        self.numberOfEntities = numberOfEntities
        self.logger = logging.getLogger()
        self.width = width
        self.height = height
        self.quadTree = QuadTree(Vector(width, height), Vector(0,0), tag='base')
        self.elementTracker.add(self.quadTree)
        self.activeSquaresTracker = squareTracker
        
    
    def addEntity(self, Particle):
        self.elementTracker.add(self.quadTree)
        self.quadTree.add(Particle)
        
    def undo(self):
        o = tracker.undo(self.quadTree)
        self.quadTree = o
    
    def redo(self):
        o = tracker.redo()
        if o is not None:
            self.quadTree = o
    
    def setup(self):
        for index in range(self.numberOfEntities):
            vXY = self.setupPosition()
            velocity = self.setupVelocity()
            particle = Particle(vXY, velocity)
            self.entities.append(particle)
            self.quadTree.add(particle)
        
    def setupVelocity(self):
        configVelocity = c["noVelocity"]
        
        if configVelocity == False:
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

    def getAllSquareCoordinatesSorted(self):
        # reduce amount of coordinates, since double coordinates aren't needed to correctly draw lines. 
        metaData = self.quadTree.getAllSquareMetadata()
        used = []
        biggestCoordinate = None
        
        for coordinate in metaData:
            if len(used) == 0:
                used.append(coordinate)
                biggestCoordinate = coordinate
            else:
                l = self.compare(coordinate, biggestCoordinate)
                
                if l == 0 :
                    continue
                
                if (l > 0):
                    biggestCoordinate = coordinate
                    used.append(coordinate)
                    
                if (l < 0):
                    foundPlace = False
                    beenSmaller = False
                    beenBigger = False
                    index = -1
                    
                    while(foundPlace == False or index != len(used)):
                        print({'index': index, 'usedLength': len(used)})
                        index += 1
                        v = used[index]
                        c = self.compare(coordinate, v)
                    
                        if c == 0:
                            break                     # No need to add
                        elif c == -1:
                            beenSmaller = True
                        elif c == 1:
                            beenBigger = True
    
                        if (beenSmaller and beenBigger):
                            # found a position
                            used.insert(index, coordinate)
                            foundPlace = True
                            break
        return used


    def compare(self, v1, v2):
        if v1 == v2:
            return 0
        if v1 < v2:
            return -1
        if v1 > v2:
            return 1