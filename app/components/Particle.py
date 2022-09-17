import logging
from app.config import data as config
from p5 import ellipse, fill, color as c, random_uniform, Vector
from .MovingObject import MovingObject


class Particle(MovingObject):

  def __init__(self, vXY, vVelocity):
    super().__init__(vXY, 40, 40, vVelocity)
    self.changeColor()
    self.logger = logging.getLogger()
    randomParticleSize = config["randomParticleSize"]
    
    if randomParticleSize:
      sizeMin = config["particleSizeMin"]
      sizeMax = config["particleSizeMax"]
      self.particleSize = random_uniform(sizeMax, sizeMin)
    else:
      self.particleSize = config["particleSize"]
      
    self.mass = float(self.particleSize)

  def __repr__(self) -> str:
    return f"{self.pos.x} {self.pos.y}"

  def draw(self):
    self.logger.debug('Drawing of particle')
    fill(self.color)
    ellipse(self.pos, self.particleSize, self.particleSize)
    self.move()
    
  def changeColor(self, color = None):
    if color is not None:
      self.color = color
    else:
      self.color = c.Color(random_uniform(255), random_uniform(255), random_uniform(255)) 
    