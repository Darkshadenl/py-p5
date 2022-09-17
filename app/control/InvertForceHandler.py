from app.control.ChainOfRes import AbstractHandler
import logging

class InvertForceHandler(AbstractHandler):
    
    def __init__(self, forcesConfig):
        self.forcesConfig = forcesConfig 
        self.logger = logging.getLogger('InvertForceHandler')
    
    def handle(self, request):
        if self.forcesConfig['inverted'] == True:
            for key, value in self.forcesConfig['forces'].items():
                v = -value
                self.forcesConfig['forces'][f'{key}'] = v
            self.logger.info('Forced inverted.')    
            
        self.forcesConfig['inverted'] = False
        super().handle(request)
            
            