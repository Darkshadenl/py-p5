import logging
from pprint import pprint
from app.components.Border import ParticleBorder
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
        entities = self.mainModel.quadtree.getAllEntitiesClear()
        self.draw(entities)
        self.drawBorders(entities)

    def draw(self, entities):
        for entity in entities:
            self.logger.debug('Drawing from generalController')
            entity.draw()
                
    def drawBorders(self, entities):
        if (self.enableBorders == False):
            return

        count = 0
        iterator = iter(entities)
        
        # TODO herschrijf dit. 
        while(count < len(entities)):
            particle = next(iterator)
            if not particle:
                break
            neighbours = particle.getNeighbours()
            quad = particle.quadTree
            self.__drawVectorBorder(quad.northWestCorner, quad.northEastCorner)
            self.__drawVectorBorder(quad.northEastCorner, quad.southEastCorner)
            self.__drawVectorBorder(quad.southEastCorner, quad.southWestCorner)
            self.__drawVectorBorder(quad.southWestCorner, quad.northWestCorner)
            
            count += len(neighbours)
            if len(neighbours) == 0:
                continue
            if len(neighbours) == 1:
                particle = neighbours[0]
                particle.changeColor()
                continue    
            for index in range(len(neighbours)):
                particle = neighbours[index]
                i = index + 1
                nextParticle = neighbours[i] if i < len(neighbours) else None
                self.__drawParticleBorder(particle, nextParticle) 
   
        
    
    def __drawParticleBorder(self, vP1, vP2):
        if vP2 is None:
            return
        self.__drawVectorBorder(vP1.pos, vP2.pos)
        
    def __drawVectorBorder(self, vP1, vP2):
        self.logger.debug('draw border')
        line(vP1, vP2)
        stroke("blue")
        stroke_weight(2)
        pass
    
    def mouse_pressed(self, event):
        self.logger.debug('mouse pressed')
        if c["debug"] == True:
            x = event.x
            y = event.y
            self.mainModel.quadtree.add(Particle(Vector(x, y), Vector(0, 0)))
       

    def key_pressed(self, event):
        self.logger.debug('key pressed')
        self.enableBorders = not self.enableBorders
        k = event.key.text
        
        if c["debug"] == True:
            if (k == 'd'):
                self.logger.info("clear all")
                # delete all particles
                self.mainModel.quadtree.clearAll()
                pass
            if (k == "o"):
                self.logger.info("clear one")
                self.mainModel.quadtree.clearOne()
            