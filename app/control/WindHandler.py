from app.control.ChainOfRes import AbstractHandler


class WindHandler(AbstractHandler):
    
    def __init__(self, wind):
        self.wind = wind
    
    def handle(self, request) -> str:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        else:
            return super().handle(request)