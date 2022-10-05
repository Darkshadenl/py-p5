# childIndex 0 - 3
from collections import namedtuple
from p5 import Vector

from app.dataStructures.QuadNode import QuadNode

def __zeropointCalculator(size, layer, route, zeroVector: Vector = Vector(0,0)):
    b = namedtuple('zeroPointData', ['size','route', 'zeroVector'])
    data = None                                      
    if layer > 0:
        data = __zeropointCalculator(size, layer - 1, route, zeroVector)

    if layer == 0:
        route.pop()
        d = b(size, route, zeroVector)
        return d
    
    routeNode = route.pop()
    s = data.size / 2
    v = data.zeroVector

    match routeNode:
        case 1:
            v.x += s
        case 2:
            v.y += s
        case 3:
            v.x += s
            v.y += s
    
    data = b(s, route, v)
    return data
    

def __routeToBaseSquareCalculator(square: QuadNode, route: list[int] = []):
        if square.parentIndex != -1:
            s = n[square.parentIndex]
            route = __routeToBaseSquareCalculator(s, route)
            
        route.append(square.index)
        return route
        

    
a = QuadNode(0)
b = QuadNode(1, parentIndex=0, childIndex=1)
c = QuadNode(2, parentIndex=1, childIndex=3)
d = QuadNode(3, parentIndex=2)
n = [a, b, c, d]    

m = __routeToBaseSquareCalculator(d)
m.reverse()
print(m)

# v = Vector(0,0)
print(__zeropointCalculator(400, len(m) - 1, m))

# 400 / 2 / 2 = 100. 
# 