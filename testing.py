from p5 import Vector
import time
from app.components.Particle import Particle
import app.dataStructures.QTree
import app.dataStructures.QuadElt
import app.dataStructures.QuadNode
import app.dataStructures.QuadEltNode
from numpy import zeros

p = time.perf_counter
l = [10, 20, 30, 40] 

nd = zeros(10000, dtype='u1')
l = []

for i in range(10000):
    l.append(0)


def timer(target, note = 'time'):
    a = p()
    target()
    b = p()
    y = b - a
    print(f"{note}: {y}")

def old():
    a, b, c, d = 0, 20, 20, 40
    x, y = 10, 10
    if x >= a and y >= b and x <= c and y <= d:
        print("True") 
    else:
        print("False")

def v():
    contender = Vector(300, 300)
    tL = Vector(200, 200)
    bR = tL + Vector(200, 200)
    
    if contender <= bR and contender >= tL:
        print(True)
    else:
        print(False)
   
def time_insertion_based_on_length():
    i = len(l) 
    l.insert(i, 100)  

def time_insertion_based_on_append():
    l.append(300)

# timer(old)
# timer(v)
# timer(time_insertion_based_on_length, 'length')
# timer(time_insertion_based_on_append, 'append')

def getFromNdarray():
    e = nd[500]
    
def getFromList():
    e = l[500]
    
timer(getFromNdarray, 'ndarray')
timer(getFromList, 'list')