from tile import Tile


class Start(Tile):
  def render(self):
    return "start"
  
  def start(self):
    self.here = False
