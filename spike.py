from tile import Tile
from pyworld.locals import *
from pygame.event import Event


class Spike(Tile):
  def render(self):
    return "spike"
  
  def hit(self, obj, dir):
    self.tilemap.event(Event(HURT))
