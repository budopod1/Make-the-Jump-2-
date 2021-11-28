from tile import Tile
from pyworld.locals import *
from direction import Direction
from pygame.event import Event
from math import cos
from time import time


class MovingUD(Tile):
  def render(self):
    return "movingud"
  
  def start(self):
    self.start_time = time()
    self.snoap = True
    self.tilemap.game.on(TICK, self.tick)
  
  def tick(self, evt):
    self.yv = cos((time() - self.start_time) * 2) * 2
    self.y = self.y + self.yv * self.tilemap.game.time_delta
  
  def colliding(self, x, y):
    return y < 0.1
  
  def hit(self, obj, dir):
    if dir == Direction.UP:
      if obj.y - self.y > -0.5:
        self.tilemap.event(Event(HURT))
