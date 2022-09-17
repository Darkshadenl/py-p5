from app.control.ChainOfRes import AbstractHandler


class InvertForceHandler(AbstractHandler):
    
    def __init__(self, gravity):
        self.gravity = gravity 
    
    def handle(self, request) -> str:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        else:
            return super().handle(request)