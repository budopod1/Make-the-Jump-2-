from tile import Tile
from time import time
from pyworld.locals import *
from direction import Direction


class Bridge(Tile):
  STRENGTH = 0.5

  def __init__(self):
    super().__init__()
    self.break_time = float("inf")
  
  def start(self):
    self.tilemap.game.on(TICK, self.tick)
  
  def tick(self, event):
    if self.break_time < time():
      self.here = False

  def render(self):
    return "bridge"
  
  def hit(self, obj, dir):
    if dir == Direction.DOWN and self.break_time == float("inf"):
      self.break_time = time() + self.STRENGTH
  
  def colliding(self, x, y):
    return y < 0.1
