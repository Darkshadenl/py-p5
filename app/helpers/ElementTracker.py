import numpy as np
import copy 

class ElementTracker:
    
    def __init__(self) -> None:
        self.list = np.empty(0)
        self.redoList = np.empty(0)
    
    def add(self, element):
        e = copy.deepcopy(element)
        self.list = np.append(self.list, e)
        
        if len(self.list) > 5:
            self.list = np.delete(self.list, 0)
    
    def undo(self, element):
        if len(self.list) > 1:
            l = self.list[-1]
            
            print(("before", {'redoList': len(self.redoList), 'list': len(self.list)}))
            
            self.redoList = np.append(self.redoList, element)
            self.list = np.delete(self.list, -1)
            
            print(("after", {'redoList': len(self.redoList), 'list': len(self.list)}))
            
            if len(self.redoList) > 3:
                self.redoList = np.delete(self.redoList, 0)
                
            return l
        else:
            return self.list[0]
    
    def redo(self):
        if len(self.redoList) >= 1:
            print(("before", {'redoList': len(self.redoList), 'list': len(self.list)}))
            
            e = self.redoList[-1]
            
            try: 
                self.list = np.append(self.list, self.redoList[-2])
            except:
                self.list = np.append(self.list, self.redoList[-1])
                
            self.redoList = np.delete(self.redoList, -1)
            
            print(("after", {'redoList': len(self.redoList), 'list': len(self.list)}))
            
            return e
        else:
            return None
        

tracker = ElementTracker()