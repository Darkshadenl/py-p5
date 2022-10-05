import sys
from p5 import *
import logging
from app.config import data as app_config
from app.GeneralController import GeneralController 
from concurrent.futures import ThreadPoolExecutor as Executor


logger = logging.getLogger() 
backgroundColor = app_config.get("canvasBackgroundColor")
width = app_config.get("canvasWidth")
height = app_config.get("canvasHeight")
numberOfEntities = app_config.get("numberOfEntities")

entities = []
controller = GeneralController(width, height, numberOfEntities)


def setup():
  logger.info("setup")
  title("Balls")
  size(width, height)
  background(backgroundColor)
    

def draw():
  background(backgroundColor)
  controller.update()

def mouse_pressed(event):
  controller.mouse_pressed(event)
  
def key_pressed(event):
  controller.key_pressed(event)

if __name__ == "__main__":
  try:
    logging.basicConfig(level=logging.INFO) 
    with Executor(max_workers=5) as exe:  
            exe.submit(run)
  except:
    print('bye')
    sys.exit()