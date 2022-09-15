import logging
import sys
from p5 import Vector, random_uniform
import unittest
from app.components.Particle import Particle
from app.dataStructures.QuadTree import QuadTree
from app.config import data as c
from unittest.mock import MagicMock

from app.model.MainModel import MainModel


class TestQuad(unittest.TestCase):
     
    @classmethod
    def setUpClass(cls): 
        logger = logging.getLogger()
        logger.level = logging.DEBUG
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
     
    def setUp(self) -> None:        
        self.q = QuadTree(Vector(200, 200), Vector(0,0), tag='base')
    
    def test_subdivides_after_set_number(self):
        for index in range(c["subdivideCount"] + 10):
            v = Vector(random_uniform(0, 199), random_uniform(0, 199))
            self.q.add(Particle(MagicMock(), v, v))
        
        self.assertEqual(True, self.q.subdivided)
        
    
    def test_subdivides_correctly_one(self):
        self.q.add(Particle(MagicMock(), Vector(10, 10), Vector(10, 10)))
        self.q.add(Particle(MagicMock(), Vector(20, 10), Vector(20, 10)))
        self.q.add(Particle(MagicMock(), Vector(30, 10), Vector(30, 10)))
        self.q.add(Particle(MagicMock(), Vector(40, 10), Vector(40, 10)))
        
        all = self.q.getAllEntities()
        northWestLevel3 = all[1][1][1]["length"]
        northEastLevel3 = all[1][1][2]["length"]
        
        self.assertEqual(northWestLevel3, 2)
        self.assertEqual(northEastLevel3, 2)
        
    
    def test_subdivides_correctly_two(self):
        self.q.add(Particle(MagicMock(), Vector(190, 190), Vector(190, 190)))
        self.q.add(Particle(MagicMock(), Vector(191, 190), Vector(191, 190)))
        self.q.add(Particle(MagicMock(), Vector(192, 190), Vector(192, 190)))
        self.q.add(Particle(MagicMock(), Vector(193, 190), Vector(193, 190)))
        
        all = self.q.getAllEntities()
        southEastLevel3 = all[3][3][3]["length"]
        self.assertEqual(southEastLevel3, 4)

    def test_add_to_already_subdivided(self):
        self.q.add(Particle(MagicMock(), Vector(10, 10), Vector(10, 10)))
        self.q.add(Particle(MagicMock(), Vector(11, 10), Vector(11, 10)))
        self.q.add(Particle(MagicMock(), Vector(12, 10), Vector(12, 10)))
        self.q.add(Particle(MagicMock(), Vector(13, 10), Vector(13, 10)))
        
        self.q.add(Particle(MagicMock(), Vector(14, 10), Vector(14, 10)))
        
        all = self.q.getAllEntities()
        northWestLevel3 = all[1][1][1]["length"]
        
        self.assertEqual(northWestLevel3, 5)
        
    def test_desplit_from_level_one(self):
        nwV = Particle(MagicMock(), Vector(10, 10), Vector(10, 10))
        self.q.add(nwV)
        self.q.add(Particle(MagicMock(), Vector(11, 10), Vector(11, 10)))
        self.q.add(Particle(MagicMock(), Vector(55, 10), Vector(55, 10)))
        self.q.add(Particle(MagicMock(), Vector(58, 10), Vector(58, 10)))
        
        all = self.q.getAllEntities()
        square = all[1][1]["self"] 
        square.removeEntity(nwV)
        square.parent.desplitCheck()
        all = self.q.getAllEntities()
        depthOneNorthWest = all[1][1]["length"]
        depthOneNorthEast = all[1][2]["length"]
        
        self.assertEqual(depthOneNorthEast, 2)
        self.assertEqual(depthOneNorthWest, 1)
        
        
    def test_desplit_from_level_two(self):
        particles = [
            Particle(Vector(108, 10), Vector(108, 10)),
            Particle(Vector(109, 10), Vector(109, 10)),
            Particle(Vector(152, 10), Vector(110, 10)),
            Particle(Vector(160, 10), Vector(111, 10)),
            Particle(Vector(50, 10), Vector(112, 10)),
            Particle(Vector(50, 10), Vector(113, 10))
        ]
        
        for v in particles:
            self.q.add(v)
        
        all = self.q.getAllEntities()
        square = all[2][1]["self"] 
        square.removeEntity(particles[0])
        square.removeEntity(particles[1])  
        square.parent.desplitCheck()
        all = self.q.getAllEntities()
        
        baseLevelNorthWestLength = all[1]["length"]
        levelOneNorthEastLength = all[2][2]["length"]
        
        self.assertEqual(baseLevelNorthWestLength, 2)
        self.assertEqual(levelOneNorthEastLength, 2)
        
    def test_get_square_metadata(self):
        numberOfEntities = 20
        mainModel = MainModel(400, 400 , numberOfEntities)
        
        for index in range(numberOfEntities):
            vXY = mainModel.setupPosition()
            velocity = mainModel.setupVelocity()
            particle = Particle(vXY, velocity)
            self.q.add(particle)
        
        metaData = self.q.getAllSquareMetadataFlat()
        self.assertEqual(40, len(metaData))
        
    
    def test_order_of_sorted_squares(self):
        mainModel = MainModel(400, 400 , 4)
        p1 = Particle(Vector(100, 0, 0), Vector(0,0,0))
        p2 = Particle(Vector(100, 200, 0), Vector(0,0,0))
        p3 = Particle(Vector(50, 200, 0), Vector(0,0,0))
        p4 = Particle(Vector(50, 300, 200), Vector(0,0,0))
        
        mainModel.quadTree.add(p1)
        mainModel.quadTree.add(p2)
        mainModel.quadTree.add(p3)
        mainModel.quadTree.add(p4)
        
        metaData = mainModel.getAllSquareCoordinatesSorted()
        
        expected = [
            Vector(0,0,0),
            Vector(0,400,0),
            Vector(400,0,0),
            Vector(400,400,0)
        ]
        
        self.assertEqual(metaData, expected)
        
        
        

        
    