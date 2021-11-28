from tile import Tile
from player import Player
from pyworld.locals import *
from pygame.event import Event


class End(Tile):
  def __init__(self):
    self.render_mode = "maker"
    super().__init__()

  def render(self):
    return "end" if self.render_mode == "maker" else "choclate"
  
  def start(self):
    self.render_mode = "play"
  
  def hit(self, obj, dir):
    if isinstance(obj, Player):
      self.tilemap.game.event(Event(FINISH))
