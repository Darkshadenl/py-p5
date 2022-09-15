import logging
from p5 import *
from app.components.Particle import Particle
from model.MainModel import MainModel
from app.config import data as c

class GeneralController:
    
    def __init__(self, width, height, numberOfEntities) -> None:
        self.logger = logging.getLogger()
        self.width = width
        self.height = height
        self.enableBorders = False
        self.mainModel = MainModel(width, height, numberOfEntities)
        self.mainModel.setup()
        
    def update(self):
        entities = self.mainModel.quadTree.getAllEntitiesClear()
        self.draw(entities)
        self.drawBorders()

    def draw(self, entities):
        for entity in entities:
            self.logger.debug('Drawing from generalController')
            entity.draw()
                
    def drawBorders(self):
        if (self.enableBorders == False):
            return
        
        squareMetaData = self.mainModel.quadTree.getAllSquareMetaDataGrouped([])
        
        for metaData in squareMetaData:
            self.__drawVectorBorder(metaData.northWestCorner, metaData.northEastCorner)
            self.__drawVectorBorder(metaData.northEastCorner, metaData.southEastCorner)
            self.__drawVectorBorder(metaData.southEastCorner, metaData.southWestCorner)
            self.__drawVectorBorder(metaData.southWestCorner, metaData.northWestCorner)
   
        
    def __drawParticleBorder(self, vP1, vP2):
        if vP2 is None:
            return
        self.__drawVectorBorder(vP1.pos, vP2.pos)
        
    def __drawVectorBorder(self, vP1, vP2):
        self.logger.debug('draw border')
        line(vP1, vP2)
        stroke("blue")
        stroke_weight(2)
        
    
    def mouse_pressed(self, event):
        self.logger.debug('mouse pressed')
        if c["debug"] == True:
            x = event.x
            y = event.y
            
            if c["noVelocity"] == True:
                self.mainModel.addEntity(Particle(Vector(x, y), Vector(0, 0)))
            else:
                vel = Vector(random_uniform(c["velocityMin"], c["velocityMax"]),  
                          random_uniform(c["velocityMin"], c["velocityMax"]))
                self.mainModel.addEntity(Particle(Vector(x, y), vel))
                

    def key_pressed(self, event):
        self.logger.debug('key pressed')
        k = event.key.text
        
        if c["debug"] == True:
            if k == 'b':
                self.enableBorders = not self.enableBorders
            if (k == 'd'):
                self.logger.info("clear all")
                # delete all particles
                self.mainModel.quadTree.clearAll()
                pass
            if (k == "o"):
                self.logger.info("clear one")
                self.mainModel.quadTree.clearOne()
            if (k == "u"):
                # clear latest
                self.mainModel.undo()
            if k == 'r':
                self.mainModel.redo()
            