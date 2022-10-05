from numpy import zeros
from app.components.Particle import Particle

from app.quadtree.Node import Node


elements = zeros(1000, dtype=Particle)
nodes = zeros(1000, dtype=Node)

class TreeData():
    
    def __init__(self) -> None:
        self.openElement = 0
        self.openNode = 0

treedata = TreeData()

def addNode(node: Node) -> int:
    nodes[treedata.openNode] = node
    i = treedata.openNode
    treedata.openNode += 1
    return i

def addElement(element: Particle) -> int:
    elements[treedata.openElement] = element
    i = treedata.openElement
    treedata.openElement += 1
    return i