from collections import namedtuple
import logging
import app.components.Particle as particle
from app.config import data as config
from p5 import Vector
from app.helpers.ActiveSquaresTracker import squareTracker

class QuadTree:

    def __init__(self, vWidthHeight, vZeroPoint,  tag, head = None, depth = 0, parent = None):
        self.width = vWidthHeight.x
        self.height = vWidthHeight.y
        self.subDivideCount = config["subdivideCount"]
        self.logger = logging.getLogger()
        self.depth = depth
        self.tag = tag
        self.activeSquaresTracker = squareTracker
        self.tracked = False
        
        if isinstance(parent, QuadTree) or parent == None:
            self.parent = parent
        else:
            raise TypeError("parent should be of type None or Quadtree")
        
        if isinstance(head, QuadTree) or head == None:
            self.head = head
        else:
            raise TypeError("head should be of type None or Quadtree")

        self.zeroPoint = vZeroPoint
        self.northWestCorner = vZeroPoint
        self.northEastCorner = vZeroPoint + Vector(self.width, 0)
        self.southWestCorner = vZeroPoint + Vector(0, self.height)
        self.southEastCorner = vZeroPoint + Vector(self.width, self.height)

        self.entities = []
        self.squares = {}
        self.subdivided = False

        self.halfWidth = self.width / 2
        self.halfHeight = self.height / 2


    def __repr__(self) -> str:
        return f"{self.tag} {self.depth}"

    def add(self, entity):
        if not self.subdivided:
            self.logger.debug(f'entity with x: {entity.pos.x}')
            self.logger.debug(f'added to {self.tag} at depth {self.depth}')
            self.entities.append(entity)
            entity.setQuadTree(self)
            
            if not self.tracked:
                self.tracked = True
                self.activeSquaresTracker.add(self)
                
            if self.__shouldSubdivide():
                self.__subdivide()
                
        elif self.subdivided:
            self.__divide([entity])
    
    def __divide(self, entities):
        if not isinstance(entities, list):
            raise TypeError("object should be of type list")
        
        deleteList = []
            
        for entity in entities:
            for square in self.squares.values():
                if square.__isVectorWithinMe(entity.pos):
                    square.add(entity)
                    deleteList.append(entity)
                    break
        for e in deleteList:
            self.removeEntity(e)

    def __isVectorWithinMe(self, vector):
        lX = self.northWestCorner.x
        lY = self.northWestCorner.y
        rX = self.southEastCorner.x
        rY = self.southEastCorner.y

        vX = vector.x
        vY = vector.y
        
        if vX >= lX and vY >= lY and vX <= rX and vY <= rY:
            return True 
        return False

    def __shouldSubdivide(self):
        if len(self.entities) < self.subDivideCount:
            return False
        return True


    def __subdivide(self):
        self.subdivided = True
        
        if self.width > config["maxWHsplit"] and self.height > config["maxWHsplit"]:  
            nwZ, neZ, seZ, swZ = self.__getZeroPoints()
            widthHeightVector = Vector(self.halfWidth, self.halfHeight)
            self.squares["northWest"] = QuadTree(widthHeightVector, nwZ, "northWest", depth=self.depth + 1, parent=self, head=self.head)
            self.squares["northEast"] = QuadTree(widthHeightVector, neZ, "northEast", depth=self.depth + 1, parent=self, head=self.head)
            self.squares["southEast"] = QuadTree(widthHeightVector, seZ, "southEast", depth=self.depth + 1, parent=self, head=self.head)
            self.squares["southWest"] = QuadTree(widthHeightVector, swZ, "southWest", depth=self.depth + 1, parent=self, head=self.head)
            self.__divide(self.entities)
        else:
            # Squares getting too small. Just leave it all in entities
            self.subdivided = False
            return
        
    
    def getAllEntities(self):
        if len(self.squares) == 0:
            return {'tag:': self.tag, 'depth': self.depth, 'length': len(self.entities),
                    'entities': self.entities, 'self': self }
        
        ents = []
        for sq in self.squares.values():
            ents.append(sq.getAllEntities())
        
        ents.append(self)
        ents.insert(0, self.tag)
        return ents
    
    def getAllEntitiesClear(self):
        if not self.subdivided:
            return self.entities

        ents = []
        for sq in self.squares.values():
            ents.extend(sq.getAllEntitiesClear())
        return ents
    
    def __getZeroPoints(self):
        nwZ = self.northWestCorner
        neZ = Vector(nwZ.x + self.halfWidth, nwZ.y)
        seZ = Vector(nwZ.x + self.halfWidth, nwZ.y + self.halfHeight)
        swZ = Vector(nwZ.x, nwZ.y + self.halfHeight)
        return (nwZ, neZ, seZ, swZ)


    def removeEntity(self, entity):
        if not isinstance(entity, particle.Particle):
            raise TypeError("Only objects of type Particle allowed")
        
        try:
            self.entities.remove(entity)
            self.logger.debug(f'Removed entity. {self.getLocation()} \n entity length: {len(self.entities)}')
        except:
            self.logger.debug('Entity not in list')
        
        if len(self.entities) == 0:
            self.activeSquaresTracker.remove(self)
            self.tracked = False
        
    def desplitCheck(self):
        self.logger.debug('desplitChecking: loca: ')
        self.logger.debug(self.getLocation())
        if self.subdivided == False:
            if self.parent is not None:
                self.logger.debug('moving check to parents')
                self.parent.desplitCheck()
            return
        
        # Total amount of entities should be less than divide amount
        totalEnts = self.__getSquaresEntityAmount()
        self.logger.debug(f'Tag: {self.tag}')
        self.logger.debug(f'TotalEntities in children: {totalEnts} ///  subdivideCount: {self.subDivideCount}')
        if totalEnts < self.subDivideCount:
            self.logger.debug("desplitting")
            self.logger.debug(f'depth: {self.depth} entities: {self.entities}')
            self.__desplit()
        else:
            self.logger.debug('Splitting rejected')
            
    def checkElementInSquare(self, element) -> bool:
        if (isinstance(element, Vector)):
            return self.__isVectorWithinMe(element)
        elif(isinstance(element, particle.Particle)):
            return self.__isVectorWithinMe(element.pos)
        else:
            raise TypeError("Only objects of type  or Vector allowed")

    def __getSquaresEntityAmount(self) -> int:
        amount = 0
        for sq in self.squares.values():
            if (sq.subdivided):
                amount += sq.__getSquaresEntityAmount()
            else:
                amount += len(sq.entities)
        self.logger.debug(f'Children entity amount: {amount}')
        return amount

    def __desplit(self):
        self.logger.debug('Desplit: loca: ')
        self.logger.debug(self.getLocation())
        
        entities = self.getAllEntitiesClear()
        
        for e in entities:
            if isinstance(e, particle.Particle):
                e.setQuadTree(self)
        
        self.entities.extend(entities)
        self.clearEntitiesInChildren()
        self.logger.debug('Setting subdivided to false \n \n')
        self.subdivided = False
        self.squares = {}
        
    def clearEntitiesInChildren(self):
        if self.subdivided == False:
            self.entities.clear()
            self.activeSquaresTracker.remove(self)
            return
        
        for sq in self.squares.values():
            sq.clearEntitiesInChildren()
            
    def clearAll(self):
        if len(self.squares) > 0:
            for s in self.squares.values():
                s.clearEntitiesInChildren()
        else:
            self.entities.clear()
        
    
    def clearOne(self):
        if len(self.squares) > 0:
            for s in self.squares.values():
                s.clearOne()
        elif len(self.entities) > 0:
            self.entities.pop()
        
    
    def getAllSquareMetadataFlat(self):
        if len(self.squares) > 0:
            squareMetaData = []
            
            for square in self.squares.values():
                squareMetaData.extend(square.getAllSquareMetadata())
            
            return squareMetaData
        
        if len(self.squares) == 0:
            metadata = [
            self.northWestCorner,
            self.northEastCorner,
            self.southWestCorner,
            self.southEastCorner  ]            
            
            return metadata
            
    
    def getAllSquareMetaDataGrouped(self, data):
        metadata = namedtuple("metadata", ["northWestCorner", "northEastCorner",
                                           "southWestCorner", "southEastCorner"])
        
        if len(self.squares) == 0:
            d = metadata (
            self.northWestCorner,
            self.northEastCorner,
            self.southWestCorner,
            self.southEastCorner  )
            data.append(d)
            return data
        
        if len(self.squares) > 0: 
            # current Quad metadata + children metadata. 
                        
            for square in self.squares.values():
                data = square.getAllSquareMetaDataGrouped(data)
            
            return data
        
    def getLocation(self):
        return self.__getLocation([])
            
    def __getLocation(self, locationList) -> list:
        if isinstance(locationList, list):
            if self.parent:
                locationList = self.parent.__getLocation(locationList)     
            
            locationList.append(f"{self.tag}:{self.depth}")
            return locationList
            