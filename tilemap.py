from pyworld.obj import Obj
from pyworld.locals import *
from pygame.locals import *


class Tilemap(Obj):
  def __init__(self, game):
    super().__init__()
    self.game = game
    self.init_tiles = True
    self.tiles = {}
    self.snoap = []
  
  def snap(self, point):
    return (round(point[0]), round(point[1]))

  def render(self):
    to_remove = []
    for coord, tile in self.tiles.items():
      if not tile.here:
        to_remove.append(coord)
        continue
      self.game.draw(tile.render(), coord[0], coord[1], 1)
    for tile in self.snoap:
      # TODO: add to_remove support
      # print(tile.y)
      self.game.draw(tile.render(), tile.x, tile.y, 1)
    for tile in to_remove:
      del self.tiles[tile]
  
  def set(self, x, y, tile):
    if self.init_tiles:
      tile.tilemap = self
      tile.start()
      if tile.snoap:
        tile.x = x
        tile.y = y
        self.snoap.append(tile)
        return
    self.tiles[(x, y)] = tile
  
  def init_all_tiles(self):
    for coord, tile in dict(self.tiles).items():
      tile.tilemap = self
      tile.start()
      if tile.snoap:
        tile.x = coord[0]
        tile.y = coord[1]
        self.snoap.append(tile)
        del self.tiles[coord]
  
  def get(self, x, y):
    tiles = []
    for coord, tile in self.tiles.items():
      if abs(coord[0] - x) < 0.5 and abs(coord[1] - y) < 0.5:
        tiles.append(tile)
    for tile in self.snoap:
      # print(0, tile.y)
      if abs(tile.x - x) < 0.5 and abs(tile.y - y) < 0.5:
        # print(1, tile.y)
        tiles.append(tile)
    return tiles
  
  def remove(self, x, y):
    for tile in self.get(x, y):
      if tile.snoap:
        self.snoap.remove(tile)
      else:
        del self.tiles[(x, y)]
  
  def collision(self, x, y):
    tiles = self.get(x, y)
    if not tiles:
      return None
    for tile in tiles:
      if tile.snoap:
        if tile.colliding(x - tile.x, y - tile.y):
          return tile
      else:
        snap = self.snap((x, y))
        x -= snap[0]
        y -= snap[1]
        if tile.colliding(x, y):
          return tile
      return None
