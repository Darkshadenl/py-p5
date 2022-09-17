import logging
from p5 import *
from app.components.Particle import Particle
from app.control.ForceHandler import ForceHandler
from app.control.GravityHandler import GravityHandler
from app.control.InvertForceHandler import InvertForceHandler
from app.control.WindHandler import WindHandler
from model.MainModel import MainModel
from app.config import data as c

class GeneralController:
    
    def __init__(self, width, height, numberOfEntities) -> None:
        self.logger = logging.getLogger()
        self.width = width
        self.height = height
        enableForces = True
        invertForce = False
        applyWind = False
        gravity = Vector(0, c["gravity"])
        wind = Vector(c["wind"], 0)
        
        if c["debug"] == True:
            self.enableBorders = True
        else: 
            self.enableBorders = False
        
        self.mainModel = MainModel(width, height, numberOfEntities)
        self.mainModel.setup()
        
        self.forceBooleans = {
            "enabled": enableForces,
            "inverted": invertForce,
            "applyWind": applyWind, 
            "wind": wind,
            "gravity": gravity
        }
        
        self.handlerSetup()
        
    def handlerSetup(self):
        fb = self.forceBooleans
        fHandler = ForceHandler(fb['enabled'])
        iHandler = InvertForceHandler(fb['inverted'])
        gHandler = GravityHandler(fb['gravity'])
        wHandler = WindHandler(fb['wind'])
        
        fHandler.set_next(iHandler).set_next(gHandler).set_next(wHandler)
        self.handler = fHandler
        
    def update(self):
        entities = self.mainModel.quadTree.getAllEntitiesClear()
        self.draw(entities)
        self.drawBorders()

    def draw(self, entities):
        for entity in entities:
            self.logger.debug('Drawing from generalController')
            
            self.handler.handle()
            
            # if self.enableForces:
            #     entity.applyForce(self.gravity)
            #     # entity.applyForce(self.wind)
            #     if self.invertForce:
            #         self.wind = -self.wind
            #         self.gravity = -self.gravity
            #         self.invertForce = False
                
            entity.draw()
                
    def drawBorders(self):
        if (self.enableBorders == False):
            return
        
        # squareMetaData = self.mainModel.quadTree.getAllSquareMetaDataGrouped([])
        self.mainModel.activeSquaresTracker.refresh()
        squareMetaData = self.mainModel.activeSquaresTracker.active
        
        for metaData in squareMetaData:
            self.__drawVectorBorder(metaData.northWestCorner, metaData.northEastCorner)
            self.__drawVectorBorder(metaData.northEastCorner, metaData.southEastCorner)
            self.__drawVectorBorder(metaData.southEastCorner, metaData.southWestCorner)
            self.__drawVectorBorder(metaData.southWestCorner, metaData.northWestCorner)
            
            if len(metaData.entities) >= 2:
                ents = metaData.entities
                for i in range(0, len(ents)):
                    try:                        
                        self.__drawParticleBorder(ents[i], ents[i + 1])
                    except:
                        self.__drawParticleBorder(ents[i], ents[0])
   
                    
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
        self.applyWind = True
        
        if c["debug"] == True:
            x = event.x
            y = event.y
            
            if c["noVelocity"] == True:
                self.mainModel.addEntity(Particle(Vector(x, y), Vector(0, 0)))
            elif c["noVelocity"] == False:
                vel = Vector(random_uniform(c["velocityMin"], c["velocityMax"]),  
                          random_uniform(c["velocityMin"], c["velocityMax"]))
                self.mainModel.addEntity(Particle(Vector(x, y), vel))
                
    def mouse_released(self, event):
        self.applyWind = False

    def key_pressed(self, event):
        self.logger.debug('key pressed')
        k = event.key.text
        if k == 'b':
            self.enableBorders = not self.enableBorders
        if k == '5':
            self.logger.info('refreshing active squares')
            self.mainModel.activeSquaresTracker.refresh()
        
        if k == 'f':
            self.enableForces = not self.enableForces
        if k == 's':
            # invert forces
            self.invertForce = True
        
        if c["debug"] == True:
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
            if k == '1':
                self.logger.info('\nAllEnts')
                print(len(self.mainModel.quadTree.getAllEntitiesClear()))
            