import numpy as np
import logging

import app.dataStructures.QuadTree as q

class ActiveSquaresTracker:
    
    def __init__(self) -> None:
        self.active = np.empty(0)
        self.logger = logging.getLogger('ActiveSquaresTracker')
        
    def add(self, square):
        if (isinstance(square, q.QuadTree)):
            self.active = np.append(self.active, square)
        
    def remove(self, square):
        if len(self.active) < 1:
            return
        
        try:
            if isinstance(square, q.QuadTree):
                for i in range(0, len(self.active)-1):
                    if self.active[i] == square:
                        self.active = np.delete(self.active, i)
            
            elif isinstance(square, list):
                for s in square:
                    for i in range(0, len(self.active)-1):
                        if self.active[i] == s:
                            self.active = np.delete(self.active, i)
        except Exception as e:
            self.logger.warning(e)
            self.logger.warning('Removing from activesquares failed. Moving on...')
            self.logger.warning(f'Active squares {self.active}')
                                
    def refresh(self):
        for i in range(0, len(self.active)-1):
            if len(self.active[i].entities) == 0:
                self.active = np.delete(self.active, i)
                

squareTracker = ActiveSquaresTracker()