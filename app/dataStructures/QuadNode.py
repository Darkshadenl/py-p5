class QuadNode:
    def __init__(self, index = -1, 
                 first_child: int = -1,
                 count: int = 0,
                 layer: int = -1,
                 childIndex: int = 0,
                 parentIndex: int = -1):
        self.index = index
        self.parentIndex = parentIndex
        self.first_child = first_child
        self.first_element = -1
        self.childIndex = childIndex
        self.count = count
        self.layer = layer
        self.oldCount = 0
        # calculate layer as you go
    
            