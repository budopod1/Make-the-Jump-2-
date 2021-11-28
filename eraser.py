from tile import Tile


class Eraser(Tile):
  def render(self):
    self.here = False
    return "eraser"
