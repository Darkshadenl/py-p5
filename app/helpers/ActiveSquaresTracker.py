import numpy as np

class ActiveSquaresTracker:
    
    def __init__(self) -> None:
        self.active = np.empty(0)
        
    def add(self, square):
        self.active = np.append(self.active, square)
        
    def remove(self, square):
        if len(self.active) > 0:
            
            for i in range(0, len(self.active)-1):
                if self.active[i] == square:
                    self.active = np.delete(self.active, i)
                    

squareTracker = ActiveSquaresTracker()