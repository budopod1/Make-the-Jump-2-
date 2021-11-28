from pyworld.obj import Obj
from pyworld.locals import *
from pygame.locals import *


class Tile(Obj):
  def __init__(self):
    self.here = True
    self.tilemap = None
    self.x = 0
    self.y = 0
    self.xv = 0
    self.yv = 0
    self.snoap = False
  
  def start(self):
    pass

  def render(self):
    return "null"

  def hit(self, obj, dir):
    pass
  
  def colliding(self, x, y):
    return True
