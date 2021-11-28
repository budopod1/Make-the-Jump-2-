import pygame
from pygame.locals import *
from pyworld.locals import *


class Events:
  def __init__(self, game):
    self.screen = None
    self.game = game
  
  def other(self, screen):
    self.screen = screen
  
  def data(self):
    events = pygame.event.get()
    new_events = []
    for event in events:
      # if event.type == KEYDOWN:
      #   print({v: k for k, v in pygame.locals.__dict__.items() if isinstance(v, int)}[event.key])

      if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
        is_gui = False
        if event.type == MOUSEBUTTONDOWN:
          for id, gui in self.screen.guis.items():
            if gui.collidepoint(pygame.mouse.get_pos()):
              new_events.append(pygame.event.Event(PRESS, {"gui": id}))
              is_gui = True
        
        if is_gui:
          continue

        event_dict = event.__dict__
        event_dict["mouse_pos"] = self.screen.screenToTile(pygame.mouse.get_pos())
        new_events.append(pygame.event.Event(event.type, event_dict))
      else:
        new_events.append(event)
      
    return new_events
  
  def start(self):
    pass
