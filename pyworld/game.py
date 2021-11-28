from pygame.event import Event
from pygame.time import Clock
from pyworld.obj import Obj
from pyworld.locals import *
from pygame.locals import *


class Game(Obj):
  def __init__(self):
    super().__init__()
    self.clock = Clock()

    self.io = None
    
    self.running = True
    self.tile_res = 50
    self.time_delta = 0
    self.data = None
    self.cam = {"x": 0, "y": 0, "size": 5}
    self.title = "Pyworld Window"

    self.on(QUIT, self.exit)
  
  def exit(self, event):
    self.running = False
  
  def start(self):
    self.io.start()

    while self.running:
      self.data = {"drawings": [], "guis": [], "texts": [], "background": (0, 0, 0), "title": self.title}
      events = self.io.data_in()

      for event in events:
        self.event(event)
      
      self.clock.tick()
      self.time_delta = self.clock.get_time() / 1000

      self.event(Event(TICK))
      self.event(Event(LATE_TICK))

      self.io.data_out(self.data)
  
  def draw(self, image, x, y, scale=1, hflip=False, vflip=False):
    self.data["drawings"].append({"image": image, "position": (x, y), "scale": scale, "flip": (hflip, vflip)})
  
  def gui(self, id, image, x, y, scale=1, hflip=False, vflip=False):
    self.data["guis"].append({"id": id, "image": image, "position": (x, y), "scale": scale, "flip": (hflip, vflip)})
  
  def text(self, text, color, x, y, scale=1, hflip=False, vflip=False):
    self.data["texts"].append({"text": text, "position": (x, y), "scale": scale, "flip": (hflip, vflip), "color": color})
  
  def background(self, color):
    self.data["background"] = color
