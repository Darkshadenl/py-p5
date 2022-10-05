import logging
from p5 import Vector, line, stroke, stroke_weight, random_uniform
from app.components.Particle import Particle
from app.control.ForceHandler import ForceHandler
from app.control.GravityHandler import GravityHandler
from app.control.InvertForceHandler import InvertForceHandler
from app.control.WindHandler import WindHandler
from model.MainModel import MainModel
from app.config import data as c
import time

class GeneralController:
    
    def __init__(self, width, height, numberOfEntities) -> None:
        self.logger = logging.getLogger('GeneralController')
        self.width = width
        self.height = height
        applyWind = True
        enableForces = True
        invertForce = False
        increaseWind = False
        decreaseWind = False
        increaseGravity = False
        decreaseGravity = False
        gravity = Vector(0, c["gravity"])
        wind = Vector(c["wind"], 0)
        
        if c["debug"] == True:
            self.enableBorders = True
        else: 
            self.enableBorders = False
        
        self.mainModel = MainModel(width, height, numberOfEntities)
        self.mainModel.setup()
        
        self.forcesConfig = {
            "enabled": enableForces,
            "inverted": invertForce,
            "applyWind": applyWind, 
            'increaseWind': increaseWind,
            'increaseGravity': increaseGravity,
            'decreaseWind': decreaseWind,
            'decreaseGravity': decreaseGravity,
            "forces": {
                "wind": wind,
                "gravity": gravity
            }
        }
        
        self.handlerSetup()
    
    def handlerSetup(self):
        fb = self.forcesConfig
        fHandler = ForceHandler(fb)
        iHandler = InvertForceHandler(fb)
        gHandler = GravityHandler(fb)
        wHandler = WindHandler(fb)
        
        fHandler.set_next(iHandler).set_next(gHandler).set_next(wHandler)
        self.handler = fHandler
        
    def update(self):
        entities : list[Particle] = self.mainModel.entities
        
        # with self.p as p:
        #     self.p.map(self.handler.handle, entities)
        #     self.p.
        start_t = time.perf_counter()
        self.draw(entities)
        end_t = time.perf_counter()
        dur = end_t - start_t
        # self.logger.info(f'Draw took: {dur}')
        self.drawBorders()

    def draw(self, entities: list[Particle]):
        counter = time.perf_counter
        for entity in entities:
            self.logger.debug('Drawing from generalController')
            self.handler.handle(entity)
            
            ent_t_s = counter() # TODO remove
            entity.draw()
            ent_t_e = counter() # TODO remove
            
            ent = ent_t_e - ent_t_s # TODO remove
            # self.logger.info(f"drawTime: {round(ent, 5)}") # TODO remove
                
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
        self.forcesConfig['applyWind'] = True
        
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
        self.forcesConfig['applyWind'] = False

    def key_pressed(self, event):
        self.logger.debug('key pressed')
        
        k = event.key.text
        
        if k == '':
            k = event.key.name
        
        if k == 'b':
            self.enableBorders = not self.enableBorders
        if k == '5':
            self.logger.info('refreshing active squares')
            self.mainModel.activeSquaresTracker.refresh()
        
        if k == 'f':
            self.forcesConfig['enabled'] = not self.forcesConfig['enabled']
            self.logger.info(f'Forces: {self.forcesConfig["enabled"]}')
        if k == 'i':
            self.forcesConfig['inverted'] = True
        if k == 'w':
            self.forcesConfig['applyWind'] = not self.forcesConfig['applyWind']
            enabled = self.forcesConfig['applyWind']
            message = 'Wind enabled' if enabled == True else 'Wind disabled.'
            self.logger.critical(message)
            
        if k == 'UP':
            self.forcesConfig['increaseGravity'] = True
        if k == 'DOWN':
            self.forcesConfig['decreaseGravity'] = True
        if k == 'RIGHT':
            self.forcesConfig['increaseWind'] = True
        if k == 'LEFT':
            self.forcesConfig['decreaseWind'] = True
        
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
            