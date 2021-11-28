from pyworld.key import Key
from controls import Controls, button
from pygame.locals import *
from pyworld.locals import *
from tile import Tile

from ground import Ground
from spike import Spike
from spring import Spring
from bridge import Bridge
from end import End
from start import Start
from eraser import Eraser
from movingud import MovingUD
from movinglr import MovingLR


class Maker:
  def __init__(self, game, tilemap):
    self.game = game
    self.tilemap = tilemap
    self.up = Key(game, button(Controls.UP))
    self.left = Key(game, button(Controls.LEFT))
    self.right = Key(game, button(Controls.RIGHT))
    self.down = Key(game, button(Controls.DOWN))
    self.speed = 2.5

    self.materials = [Ground, Spike, Spring, Bridge, MovingUD, MovingLR, Start, End, Eraser]
    self.example_materials = [[mat().render(), mat] for mat in self.materials]
    self.material = self.materials[0]

    game.on(MOUSEBUTTONDOWN, self.click)
    game.on(PRESS, self.press)
  
  def tick(self):
    if self.active:
      if self.down.down:
        self.game.cam["y"] += self.speed * self.game.time_delta
      if self.up.down:
        self.game.cam["y"] -= self.speed * self.game.time_delta
      if self.left.down:
        self.game.cam["x"] -= self.speed * self.game.time_delta
      if self.right.down:
        self.game.cam["x"] += self.speed * self.game.time_delta
      
      mat_num = 0
      for material in self.example_materials:
        yPos = (mat_num + 1) / (len(self.example_materials) + 1)
        self.game.gui(material[0] + "s", material[0], 0.1, yPos, 0.6)
        mat_num += 1
      
  
  def click(self, evt):
    if self.active:
      if evt.button == 1:
        x, y = evt.mouse_pos
        x = round(x)
        y = round(y)
        self.tilemap.set(x, y, self.material())
  

  def press(self, evt):
    if self.active:
      for mat in self.example_materials:
        if evt.gui == mat[0] + "s":
          self.material = mat[1]
