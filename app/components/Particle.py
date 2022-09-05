import logging
from tkinter.messagebox import NO
from app.config import data as config
from p5 import ellipse, fill, color as c, random_uniform
from .MovingObject import MovingObject

class Particle(MovingObject):

  def __init__(self, vXY, vVelocity):
    super().__init__(vXY, 40, 40, vVelocity)
    self.changeColor()
    self.logger = logging.getLogger()

  def draw(self):
    self.logger.debug('Drawing of particle')
    particleSize = config["particleSize"]
    fill(self.color)
    ellipse(self.pos, particleSize, particleSize)
    self.move()
    
  def changeColor(self, color = None):
    if color is not None:
      self.color = color
    else:
      self.color = c.Color(random_uniform(255), random_uniform(255), random_uniform(255)) 
    