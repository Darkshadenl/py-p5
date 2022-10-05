from collections import namedtuple
from app.dataStructures.QuadNode import QuadNode
from app.dataStructures.QuadElt import QuadElt
from app.dataStructures.QuadEltNode import QuadEltNode
import app.components.Particle as P
from app.dataStructures.QuadRectangle import QuadRectangle
from p5 import Vector

class QTree:
    def __init__(self, size):
        if size % 2 != 0:
            raise Exception("Size should be dividable by 2")
        
        self.elements : list[P.Particle] = []
        self.elt_nodes : list[QuadEltNode] = []
        self.nodes : list[QuadNode] = []
        self.size = size
        self.root_rect = QuadRectangle(size, zeroPoint=0)
        self.max_depth = 4
        self.baseNode = QuadNode(0, layer=0, childIndex=0)
        self.nodes.append(self.baseNode)
        self.freeNode = 0
        self.deleteList = []
        self.added = 0
        
        
    def add(self, element: P.Particle):
        self.added += 1
        if self.root_rect.intersectFromZeropoint(element.pos):
            index = self.__addToElements(element)
            # intersects
            quadNode = self.__findQuadNode(self.baseNode, element.pos, 0)
            
           # verify quadnode and if needed find a new one. 
            verified_Quadnode = self.__refindQuadnodeIfNeeded(quadNode, element.pos, index)
            
            # add.
            self.__addParticleToNode(verified_Quadnode, index)
            
        else:
            return
       
     
    # always after a split   
    def __reAdd(self, elt_nodeIndex: int):
        elt_node = self.elt_nodes[elt_nodeIndex]
        el = self.elements[elt_node.elementIndex]
        quad = self.nodes[elt_node.quadIndex]
        quadNode = self.__findQuadNode(startNode = quad, 
                                       elementPos = el.pos, 
                                       elIndex = elt_node.elementIndex,
                                       layer = quad.layer)
        
        # quadNode could still be full! Check first.
        verified_Quadnode = self.__refindQuadnodeIfNeeded(quadNode, el.pos, elt_node.elementIndex)            
        
        # checked. Now create new eltnode and link it. 
        linked = self.__linkEltNodes(verified_Quadnode, elt_node)
        
        if not linked:
            # quad does not have child elements yet. 
            verified_Quadnode.first_element = elt_node.selfIndex
            
        elt_node.quadIndex = verified_Quadnode.index
        verified_Quadnode.count += 1
        
        
    def __linkEltNodes(self, quadNode: QuadNode, new_node: QuadEltNode):
        # if quad already has node, get last node
        if quadNode.first_element != -1:
            lastElement = self.__retrieveLastNodeElementIndexQuadNode(quadNode)
            last_eltNode = self.elt_nodes[lastElement]
            
            new_eltNode = QuadEltNode(quadIndex=quadNode.index,
                                      previousIndex=last_eltNode.selfIndex)
            i = self.__addToEltNodes(new_eltNode)
            new_eltNode.selfIndex = i
            last_eltNode.nextIndex = new_eltNode.selfIndex
            return new_eltNode
        return False
        
    def __refindQuadnodeIfNeeded(self, quadNode: QuadNode, elPos, elIndex) -> QuadNode:
        if quadNode.layer == self.max_depth:
            return quadNode
        
        maxLayerReached = False
        while quadNode.count + 1 == 5 or maxLayerReached == True:
                n = self.__split(quadNode, True)
                # so node is now unavailable. Refind a valid quadNode.
                quadNode = self.__findQuadNode(n, elPos, elIndex, 
                                               quadNode.layer)
                if quadNode.layer == self.max_depth:
                    maxLayerReached = True
        return quadNode
        
    def __findQuadNode(self, 
                       startNode: QuadNode,
                       elementPos: Vector, 
                       elIndex: int, 
                       layer: int = 0) -> QuadNode:
        if layer == 0 and startNode.layer != -1:
            layer = startNode.layer
        
        if startNode.first_child == -1 and startNode.count + 1 != 5 and startNode.count > -1:
            # startnode is available.
            # no children, and room inside self. 
            return startNode
        
        if startNode.first_child == -1 and startNode.count + 1 == 5:
            # return but should split
            return startNode
        
        route = self.__routeToBaseSquareCalculator(startNode)
        zeroPointData = self.__zeropointCalculator(self.size, startNode.layer, route)
        midPoint = self.__midPointCalculator(zeroPointData.size, zeroPointData.zeroVector)
        # midPoint = self.__midZeropointCalculator(layer, startNode.childIndex) # TODO fix midpoint.
        qRectangle = QuadRectangle(self.size, midPoint = midPoint, vZeroPoint=zeroPointData.zeroVector)
        # pos = tL || tR || bL || bR
        pos = qRectangle.intersectFromMidpoint(elementPos, self.added)
        quadNode = self.nodes[startNode.first_child + pos]
        # if children not full, return quadnode.
        if quadNode.count + 1 != 5 and quadNode.first_child == -1:
            return quadNode
        
        if quadNode.first_child != -1:
            # quad has children so search child
            return self.__findQuadNode(quadNode, elementPos, elIndex, layer + 1)
        
        if quadNode.count + 1 == 5 and quadNode.first_child == -1:
            # correct quad found but should split
            return quadNode
        
    
    def __split(self, node: QuadNode, shouldSplit: bool = True) -> QuadNode:
        if not shouldSplit or node.layer == self.max_depth:
            return node
        
        i = len(self.nodes)
        layer = node.layer + 1
        self.nodes.insert(i, QuadNode(i, layer=layer, childIndex=0, parentIndex=node.index))          # tL
        self.nodes.insert(i + 1, QuadNode(i + 1, layer=layer, childIndex=1, parentIndex=node.index))  # tR
        self.nodes.insert(i + 2, QuadNode(i + 2, layer=layer, childIndex=2, parentIndex=node.index))  # bL
        self.nodes.insert(i + 3, QuadNode(i + 3, layer=layer, childIndex=3, parentIndex=node.index))  # bR
        node.first_child = i
        self.__divideChildren(node)
        return node
    
    def __routeToBaseSquareCalculator(self, square: QuadNode, route: list[int] = []):
        if square.parentIndex != -1:
            s = self.nodes[square.parentIndex]
            route = self.__routeToBaseSquareCalculator(s, route)
            
        route.append(square.childIndex)
        route.reverse()
        return route
    
    def __midPointCalculator(self, size, zeroVector: Vector) -> int:
        s = size / 2
        return zeroVector.x + s
    
    def __midZeropointCalculator(self, layer, childIndex):
        startPointRightx = 0
        startPointx = 0
        iterations = layer + 1
        divider = 2
        result = self.size
        
        for iteration in range(0, iterations):
            result = result // divider
        
        if layer > 0:
            if childIndex == 1 or childIndex == 3:
                startPointx = startPointRightx + result
        
        r = startPointx + result
        
        return r
    
    
    def __zeropointCalculator(self, size, layer, route):
        b = namedtuple('zeroPointData', ['size','route', 'zeroVector'])
        
        data = None                                      
        if layer > 0:
            data = self.__zeropointCalculator(size, layer - 1, route)

        if layer == 0:
            z = Vector(0,0)
            route.pop()
            d = b(size, route, z)
            return d
        
        routeNode = route.pop()
        splitSize = data.size / 2
        zeroV = data.zeroVector

        match routeNode:
            case 1:
                zeroV.x += splitSize
            case 2:
                zeroV.y += splitSize
            case 3:
                zeroV.x += splitSize
                zeroV.y += splitSize
        
        data = b(splitSize, route, zeroV)
        return data
        
    
    def __divideChildren(self, node: QuadNode):
        node.oldCount = node.count
        node.count = -1
        elements = self.__retrieveAllElements(node)
        for e in elements:
            el = self.elements[e.elementIndex]
            self.__reAdd(e.selfIndex)
            self.deleteList.append(e.selfIndex)
        node.first_element = -1
    
    def __addParticleToNode(self, node: QuadNode, pIndex: int):
        if node.count == 0:
            eltNode = QuadEltNode(pIndex, node.index)
            index = self.__addToEltNodes(eltNode)
            node.first_element = index
            node.count += 1
        elif ((node.count > 0 and node.count + 1 != 5) or (node.count > 0 
        and node.layer == self.max_depth)):
            lastElIndex = self.__retrieveLastNodeElementIndexQuadNode(node)
            lastEl = self.elt_nodes[lastElIndex]
            newLastEl = QuadEltNode(pIndex, node.index)
            newLastElIndex = self.__addToEltNodes(newLastEl)
            lastEl.nextIndex = newLastElIndex
            newLastEl.selfIndex = newLastElIndex
            newLastEl.previousIndex = lastEl.elementIndex
            node.count += 1
        else:
            raise Exception("No valid quad found. Fix __findQuadNode")

    def __addToElements(self, p: P.Particle) -> int:
        i = len(self.elements)
        self.elements.insert(i, p)
        return i
    
    def __addToEltNodes(self, eltNode: QuadEltNode) -> int:
        x = len(self.elt_nodes)
        self.elt_nodes.insert(x, eltNode)
        eltNode.selfIndex = x
        return x
    
    def __retrieveLastNodeElementIndexQuadNode(self, node: QuadNode) -> int:
        elIndex = node.first_element
        
        if elIndex == -1:
            return -1
        if elIndex > -1:
            elt = self.elt_nodes[elIndex]
            return self.__retrieveLastNodeElementIndexElementNode(elt)
            
    def __retrieveLastNodeElementIndexElementNode(self, elt: QuadEltNode) -> int:
        if elt.nextIndex == -1:
            return elt.selfIndex
        
        return self.__retrieveLastNodeElementIndexElementNode(self.elt_nodes[elt.nextIndex])
    
    def __retrieveAllElementsStart(self, index: int, els = []) -> list[QuadEltNode]:
        el = self.elt_nodes[index]
        if el.nextIndex != -1:
            els = self.__retrieveAllElementsStart(el.nextIndex, els)
        
        els.append(el)
        return els
    
    def __retrieveAllElements(self, node: QuadNode) -> list[QuadEltNode]:
        return self.__retrieveAllElementsStart(node.first_element)
        
        
        