from app.dataStructures.QuadEltNode import QuadEltNode


class QElList:
    
    def __init__(self):
        self.elements: list[QuadEltNode] = []
    
    
    # layer refers to layer of quadtree
    # nodePosition refers to tL tR bL bR
    def add(self, element: QuadEltNode,
            layer: int, nodePosition: int):
        # inputs
        # layer 1, node 0
        
        base = 1
        jump = 4
        
        if layer == 0:
            self.elements.append(element)
        
        # layer 0 = jump * 0 
        # layer 1 item 1 = base + (jump * 1)
        # layer 1 item 2 = base + (jump * 2)