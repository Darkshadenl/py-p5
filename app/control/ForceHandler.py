from app.control.ChainOfRes import AbstractHandler


class ForceHandler(AbstractHandler):
    
    def __init__(self, isForceEnabled):
        self.isForceEnabled = isForceEnabled 
    
    def handle(self, request) -> str:
        if not self.isForceEnabled:
            return
        else:
            super().handle(request)