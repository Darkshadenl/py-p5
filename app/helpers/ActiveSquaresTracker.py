import numpy as np

import app.dataStructures.QuadTree as q

class ActiveSquaresTracker:
    
    def __init__(self) -> None:
        self.active = np.empty(0)
        
    def add(self, square):
        if (isinstance(square, q.QuadTree)):
            self.active = np.append(self.active, square)
        
    def remove(self, square):
        if len(self.active) < 1:
            return
        
        if isinstance(square, q.QuadTree):
            for i in range(0, len(self.active)-1):
                if self.active[i] == square:
                    self.active = np.delete(self.active, i)
        
        elif isinstance(square, list):
            for s in square:
                for i in range(0, len(self.active)-1):
                    if self.active[i] == s:
                        self.active = np.delete(self.active, i)
                        
    def refresh(self):
        for i in range(0, len(self.active)-1):
            if len(self.active[i].entities) == 0:
                self.active = np.delete(self.active, i)
                

squareTracker = ActiveSquaresTracker()