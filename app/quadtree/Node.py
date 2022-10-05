from numpy import zeros, where
from app.quadtree.NodeData import nodeData, Rectangle
import app.quadtree.TreeData as td
from app.components.Particle import Particle
from p5 import Vector

class Node:
    
    def __init__(self, width: int, zeroPoint: Vector = Vector(0,0), layer: int= 0, index:int = 0) -> None:
        self.childNodes = zeros(4, dtype='u1')
        self.rectangle = Rectangle(zeroPoint, width)
        self.layer = layer
        self.elements = zeros(20, dtype='u1')
        self.elementCount = 0
        self.openElementIndex = 0
        self.index = 0
        self.width = width
        
    def split(self):
        self.elementCount = -1  # has split
        
        # create childnodes
        l = self.layer + 1
        a = Node(self.width / 2, self.rectangle.getTopLeft().tl, l)
        b = Node(self.width / 2, self.rectangle.getTopRight().tl, l)
        c = Node(self.width / 2, self.rectangle.getBottomLeft().tl, l)
        d = Node(self.width / 2, self.rectangle.getBottomRight().tl, l)
        
        a.index = td.addNode(a)
        b.index = td.addNode(b)
        c.index = td.addNode(c)
        d.index = td.addNode(d)
        
        self.childNodes[0] = a.index
        self.childNodes[1] = b.index
        self.childNodes[2] = c.index
        self.childNodes[3] = d.index
        
        # divide elements over childnodes
        for i in range(self.elementCount):
            elIndex = self.elements[i]
            self.__addToChild(elIndex)
        
    def addElement(self, particleIndex: int) -> None or nodeData:
        p: Particle = td.elements[particleIndex]
        
        if self.rectangle.isWithin(p.pos) == False:
            return None
        
        if self.elementCount + 1 == 4 and self.layer != 4:
            self.split()
            
        if self.elementCount == -1:
            # has already split
            self.__addToChild(particleIndex)
            
        i = self.openElementIndex
        self.elements[i] = particleIndex
        # find new opennode. if fails should crash app.
        self.openElementIndex = where(self.elements == 0)[0][0] 
        self.elementCount += 1
        return nodeData(i, self.index)
    
    
    def __addToChild(self, particleIndex):
        pos = self.rectangle.getContainerPosition(td.elements[particleIndex].pos)
        self.childNodes[pos].addElement(particleIndex)
        
    
    def removeElement(self, index: int):
        if index > len(self.elements) - 1:
            raise IndexError(index)
        
        # set element at index to 0. 
        self.elements[index] = 0
        
        # set openNode to index of element if         
        # index is before current openNode index.
        if index < self.openElementIndex:
            self.openElementIndex = index 
        
        self.elementCount -= 1
    