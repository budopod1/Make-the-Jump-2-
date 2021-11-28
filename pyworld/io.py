from pyworld.screen import Screen
from pyworld.events import Events


class IO:
  def __init__(self, game):
    self.in_manager = Events(game)
    self.out_manager = Screen(game)
    self.in_manager.other(self.out_manager)
    self.out_manager.other(self.in_manager)
  
  def data_out(self, data):
    self.out_manager.data(data)
  
  def data_in(self):
    return self.in_manager.data()
  
  def start(self):
    self.in_manager.start()
    self.out_manager.start()
  
