from app.control.ChainOfRes import AbstractHandler
from app.helpers.ParticleTypeCheck import ParticleTypeCheck

class ForceHandler(AbstractHandler):
    
    def __init__(self, forcesConfig):
        self.forcesConfig = forcesConfig 
    
    def handle(self, request):
        if not self.forcesConfig['enabled']:
            return
        else:
            super().handle(request)