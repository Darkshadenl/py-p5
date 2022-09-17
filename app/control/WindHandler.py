from app.control.ChainOfRes import AbstractHandler
from app.helpers.ParticleTypeCheck import ParticleTypeCheck
from p5 import Vector
import logging
from app.config import data as c

class WindHandler(AbstractHandler):
    
    def __init__(self, forcesConfig):
        self.forcesConfig = forcesConfig
        self.logger = logging.getLogger('WindHandler')
    
    def handle(self, request):
        p = ParticleTypeCheck(request)
        wind = self.forcesConfig['forces']['wind']
        message = ''
        
        if self.forcesConfig['increaseWind']:
            self.forcesConfig['forces']['wind'] = wind + Vector(c["windSteps"], 0)
            self.forcesConfig['increaseWind'] = False
            self.logger.info(f'Wind: {self.forcesConfig["forces"]["wind"].x}')
        
        if self.forcesConfig['decreaseWind']:
            self.forcesConfig['forces']['wind'] = wind - Vector(c["windSteps"], 0)
            self.forcesConfig['decreaseWind'] = False
            self.logger.info(f'Wind: {self.forcesConfig["forces"]["wind"].x}')

        if self.forcesConfig['applyWind']:
            p.applyForce(self.forcesConfig['forces']['wind'])
            
            
        return super().handle(request)