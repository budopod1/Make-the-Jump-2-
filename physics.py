from pyworld.obj import Obj
from pyworld.locals import *
from pygame.locals import *
from direction import to_direction, Direction


class Physics(Obj):
  def __init__(self, game, tilemap):
    super().__init__()
    self.game = game
    self.tilemap = tilemap
    self.x = 0
    self.y = 0
    self.xv = 0
    self.yv = 0
    self.xd = 0.02
    self.yd = 0.02
    self.xg = 0
    self.yg = 4
    self.reverse = False

    self.hit_points = [(0.5, 0.5), (0, 0.5), (-0.5, 0.5),
     (0.5, 0), (-0.5, 0),
      (0.5, -0.5), (0, -0.5), (-0.5, -0.5)]

    self.grounded = False
  
  def get_hits(self, x, y):
    hits = set()

    for point in self.hit_points:
      x_val = point[0]
      x_val *= -1 if self.reverse else 1
      hit = self.tilemap.collision(x + x_val, y - point[1])
      if hit:
        hits.add(hit)
    
    return hits
  
  def tick(self):
    if self.active:
      self.xv += self.xg * self.game.time_delta
      self.yv += self.yg * self.game.time_delta
      self.xv *= 1 - self.xd * self.game.time_delta
      self.yv *= 1 - self.yd * self.game.time_delta

      new_x = self.x + self.xv * self.game.time_delta
      new_y = self.y + self.yv * self.game.time_delta

      self.grounded = False

      y_hits = self.get_hits(self.x, new_y)
      if y_hits:
        oldYV = self.yv
        self.yv = 0
        for hit in y_hits:
          direction = to_direction(0, oldYV - hit.yv)
          if direction == Direction.DOWN:
            self.grounded = True
          hit.hit(self, direction)
          #if direction == Direction.DOWN:
          if hit.yv < 0:
            self.yv += hit.yv * 1.05
          # if (self.xv < hit.xv and hit.xv > 0) or (self.xv > hit.xv and hit.xv < 0):
          #   self.xv = hit.xv
          self.x += hit.xv * self.game.time_delta
          # self.y += hit.yv * self.game.time_delta
      x_hits = self.get_hits(new_x, self.y)
      if x_hits:
        oldXV = 0
        self.xv = 0
        for hit in x_hits:
          direction = to_direction(oldXV - hit.xv, 0)
          hit.hit(self, direction)
          # self.x += hit.xv * self.game.time_delta
          # self.y += hit.yv * self.game.time_delta
      
      self.x += self.xv * self.game.time_delta
      self.y += self.yv * self.game.time_delta
  