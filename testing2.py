import time
from app.components.Particle import Particle as pa
from app.dataStructures.QElList import QElList
from app.dataStructures.QTree import QTree
import app.dataStructures.QuadNode as QNode
import app.dataStructures.QuadEltNode as QElNode
from p5 import Vector, random_uniform

from app.dataStructures.QuadTree import QuadTree
from app.quadtree.Tree import Tree

l = time.perf_counter
size = 400
elements = []
subnewTree = QTree(400)
oldTree = QuadTree(Vector(400, 400), Vector(0,0), 'base')
newTree: Tree = Tree(400)

for i in range(0, 10):
    x = random_uniform(399)
    y = random_uniform(399)
    
    if i < 6:
        x = random_uniform(200, 0)
        y = random_uniform(200, 400)
    
    if i < 11 and i >= 6:
        x = random_uniform(200, 400)
        y = random_uniform(200, 400)
        
    p: pa = pa(Vector(x,y), Vector(0,0), i)
    p.id = i
    elements.append(p)

# a = l()
# for i in range(0,10):
#     subnewTree.add(elements[i])
# b = l()    
    
c = l()
for i in range(0,10):
    oldTree.add(elements[i])
d = l()

e = l()
for i in range(0,10):
    newTree.addElement(elements[i])
f = l()

# x = b - a
y = d - c
z = f - e

print(f"oldtree: {x}     newtree: {z}")
    
pass
    




