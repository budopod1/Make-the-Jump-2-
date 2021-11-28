from tile import Tile
from pyworld.locals import *
from direction import Direction
from pygame.event import Event
from math import cos
from time import time


class MovingLR(Tile):
  def render(self):
    return "movinglr"
  
  def start(self):
    self.start_time = time()
    self.snoap = True
    self.tilemap.game.on(TICK, self.tick)
  
  def tick(self, evt):
    self.xv = cos(time() - self.start_time)
    self.x = self.x + self.xv * self.tilemap.game.time_delta
  
  def colliding(self, x, y):
    return y < 0.1
