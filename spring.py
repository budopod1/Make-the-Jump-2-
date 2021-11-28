from tile import Tile
from player import Player
from direction import Direction


class Spring(Tile):
  POWER = 5

  def render(self):
    return "spring"
  
  def hit(self, obj, dir):
    if isinstance(obj, Player) and dir == Direction.DOWN:
      obj.yv = -self.POWER
