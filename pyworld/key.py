from pyworld.obj import Obj
from pygame.locals import *
from pyworld.locals import *


class Key(Obj):
  def __init__(self, game, key):
    self.game = game
    self.down = False
    self.just_down = False
    self.key = key
    self.game.on(KEYDOWN, self.key_down)
    self.game.on(KEYUP, self.key_up)
    self.game.on(LATE_TICK, self.tick)
  
  def key_down(self, evt):
    if evt.key == self.key:
      self.just_down = True
      self.down = True
  
  def tick(self, evt):
    self.just_down = False
  
  def key_up(self, evt):
    if evt.key == self.key:
      self.down = False
