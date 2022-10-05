class QuadEltNode:
    def __init__(self, elementIndex: int = -1, 
                 quadIndex = -1, 
                 nextIndex: int = -1,
                 previousIndex: int = -1):
        self.elementIndex = elementIndex
        self.quadIndex = quadIndex
        self.nextIndex = nextIndex
        self.previousIndex = previousIndex
        self.selfIndex = -1
        
    