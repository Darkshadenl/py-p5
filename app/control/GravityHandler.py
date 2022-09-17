from app.control.ChainOfRes import AbstractHandler
from app.helpers.ParticleTypeCheck import ParticleTypeCheck
from p5 import Vector
import logging
from app.config import data as c


class GravityHandler(AbstractHandler):
    
    def __init__(self, forcesConfig):
        self.forcesConfig = forcesConfig 
        self.logger = logging.getLogger('GravityHandler')
    
    def handle(self, request):
        p = ParticleTypeCheck(request)
        
        gravity = self.forcesConfig['forces']['gravity']
        
        if self.forcesConfig['increaseGravity']:
            self.forcesConfig['forces']['gravity'] = gravity + Vector(0, c["gravitySteps"])
            self.forcesConfig['increaseGravity'] = False
            self.logger.info(f'Gravity: {self.forcesConfig["forces"]["gravity"].y}')
            
        if self.forcesConfig['decreaseGravity']:
            self.forcesConfig['forces']['gravity'] = gravity - Vector(0, c["gravitySteps"])
            self.forcesConfig['decreaseGravity'] = False
            self.logger.info(f'Gravity: {self.forcesConfig["forces"]["gravity"].y}')
        
        p.applyForce(self.forcesConfig['forces']['gravity'])
        super().handle(request)
        