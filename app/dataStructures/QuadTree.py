from cmath import log
import logging
from app.helpers.ErrorObject import errorObject
from app.config import data as config
from p5 import Vector


class QuadTree:

    def __init__(self, vWidthHeight, vZeroPoint, tag, depth = 0, parent = None):
        self.width = vWidthHeight.x
        self.height = vWidthHeight.y
        self.subDivideCount = config["subdivideCount"]
        self.logger = logging.getLogger()
        self.depth = depth
        self.tag = tag
        self.parent = parent

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

    def add(self, entity):
        if not self.subdivided:
            self.logger.info(f'entity with x: {entity.pos.x}')
            self.logger.info(f'added to {self.tag} at depth {self.depth}')
            self.logger.info(entity)
            self.entities.append(entity)
            entity.setQuadTree(self)
            if self.__shouldSubdivide():
                self.__subdivide()
        elif self.subdivided:
            self.__divide([entity])
            pass

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
        if len(self.entities) <= self.subDivideCount:
            return False
        return True


    def __subdivide(self):
        self.subdivided = True
        
        if self.width > config["maxWHsplit"] and self.height > config["maxWHsplit"]:  
            nwZ, neZ, seZ, swZ = self.__getZeroPoints()
            widthHeightVector = Vector(self.halfWidth, self.halfHeight)
            self.squares["northWest"] = QuadTree(widthHeightVector, nwZ, "northWest", self.depth + 1, parent=self)
            self.squares["northEast"] = QuadTree(widthHeightVector, neZ, "northEast", self.depth + 1, parent=self)
            self.squares["southEast"] = QuadTree(widthHeightVector, seZ, "southEast", self.depth + 1, parent=self)
            self.squares["southWest"] = QuadTree(widthHeightVector, swZ, "southWest", self.depth + 1, parent=self)
            self.__divide(self.entities)
        else:
            # Squares getting too small. Just leave it all in entities
            self.subdivided = False
            return
        
    def __divide(self, ents):
        deleteList = []
            
        for entity in ents:
            for square in self.squares.values():
                if (square.__isVectorWithinMe(entity.pos)):
                    square.add(entity)
                    entity.setQuadTree(square)
                    deleteList.append(entity)
                    break
        for e in deleteList:
            self.__removeEntity(e)
    
    def getAllEntities(self):
        if len(self.squares) == 0:
            return {'tag:': self.tag, 'depth': self.depth, 'length': len(self.entities),
                    'entities': self.entities, 'self': self
                    }
        
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


    def __removeEntity(self, entity):
        try:
            self.entities.remove(entity)
        except:
            self.logger.debug('entity not in list')
        
        if (len(self.entities) == 0 and not self.subdivided):
            # Maybe desplit? Quadtree version
            self.parent.desplitCheck()
        
    def desplitCheck(self):
        if self.subdivided == False:
            if (self.parent is not None):
                self.parent.desplitCheck()
            return
        
        # Total amount of entities should be less than divide amount
        totalEnts = self.__getSquaresEntityAmount()
        if totalEnts < self.subDivideCount:
            self.logger.info("desplitting")
            self.logger.info({
                "tag": self.tag,
                "depth": self.depth,
                "entities": self.entities
            })
            self.__desplit()

    def __getSquaresEntityAmount(self) -> int:
        amount = 0
        for sq in self.squares.values():
            amount += len(sq.entities)
        return amount

    def __desplit(self):
        # if self.hasDesplit == True:
        #     return
        entities = self.getAllEntitiesClear()
        self.entities.extend(entities)
        self.clearEntitiesInChildren()
        self.subdivided = False
        self.squares = {}
        # self.hasDesplit = True
        
    def clearEntitiesInChildren(self):
        if self.subdivided == False:
            self.entities.clear()
            return
        
        for sq in self.squares.values():
            sq.clearEntitiesInChildren()
            
    def clearAll(self):
        if len(self.squares) > 0:
            for s in self.squares.values():
                s.clearEntitiesInChildren()
        else:
            self.entities.clear()
        pass
    
    def clearOne(self):
        if len(self.squares) > 0:
            for s in self.squares.values():
                s.clearOne()
        elif len(self.entities) > 0:
            self.entities.pop()
        pass