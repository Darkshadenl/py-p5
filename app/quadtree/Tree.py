from app.quadtree.TreeData import addElement, addNode
# from app.quadtree.NodeData import nodeData as n
from app.quadtree.Node import Node
from app.components.Particle import Particle

class Tree:
    
    def __init__(self, width) -> None:
        self.width = width
        self.baseNode = Node(width)
        addNode(self.baseNode)
        
        
    def addElement(self, particle: Particle):
        elI = addElement(particle) # TODO first particle index is 1 and index 0 should be value -1.
        nodedata = self.baseNode.addElement(elI)
        print(f"Added element to node at index: {nodedata.nodeIndex}.\n Elementindex {nodedata.selfIndex}")
        
        