import pygame
import pyworld.assets


class Screen:
  def __init__(self, game):
    self.title = "Error resolving connection to game."
    self.game = game
    self.screen = pygame.display.set_mode([450, 300], pygame.RESIZABLE)

    pygame.font.init()
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 64)

    self.guis = {}
  
  def other(self, evts):
    pass
  
  def start(self):
    pyworld.assets.load_assets("assets")
  
  def tileToScreen(self, pos):
    scale = (self.screen.get_height() / self.game.tile_res) / self.game.cam["size"]

    return (
      (pos[0] - self.game.cam["x"]) * self.game.tile_res * scale + self.screen.get_width() / 2,
      (pos[1] - self.game.cam["y"]) * self.game.tile_res * scale + self.screen.get_height() / 2
    )
  
  def screenToTile(self, pos):
    scale = (self.screen.get_height() / self.game.tile_res) / self.game.cam["size"]

    return (
      ((pos[0] - self.screen.get_width() / 2) / self.game.tile_res) / scale + self.game.cam["x"],
      ((pos[1] - self.screen.get_height() / 2) / self.game.tile_res) / scale + self.game.cam["y"]
    )
  
  def guiToScreen(self, pos):
    return (
      pos[0] * self.screen.get_width(),
      pos[1] * self.screen.get_height()
    )
  
  def draw(self, surface, pos, scale=1, flip=(False, False)):
    surface = pygame.transform.flip(surface, *flip)

    scale = (self.screen.get_height() / self.game.tile_res) / self.game.cam["size"] * scale
    new_height = self.game.tile_res * scale
    new_width = new_height * (surface.get_width() / surface.get_height())

    surface = pygame.transform.scale(surface, (round(new_width), round(new_height)))

    pos = self.tileToScreen(pos)

    pos = (pos[0] - surface.get_width() / 2, pos[1] - surface.get_height() / 2)

    self.screen.blit(surface, pos)

    rect = surface.get_rect()
    rect.topleft = pos
    return rect
  
  def text(self, text, color, pos, scale=1, flip=(False, False)):
    surface = self.font.render(text, True, color)
    return self.gui("text", surface, pos, scale=1, flip=(False, False))
  
  def gui(self, id, surface, pos, scale=1, flip=(False, False)):
    surface = pygame.transform.flip(surface, *flip)

    scale = (self.screen.get_height() / self.game.tile_res) / self.game.cam["size"] * scale

    new_height = self.game.tile_res * scale
    new_width = new_height * (surface.get_width() / surface.get_height())

    surface = pygame.transform.scale(surface, (round(new_width), round(new_height)))

    pos = self.guiToScreen(pos)

    pos = (pos[0] - surface.get_width() / 2, pos[1] - surface.get_height() / 2)

    self.screen.blit(surface, pos)

    rect = surface.get_rect()
    rect.topleft = pos
    self.guis[id] = rect
  
  def data(self, data):
    self.guis = {}
    if self.title != data["title"]:
      self.title = data["title"]
      pygame.display.set_caption(data["title"])
    self.screen.fill(data["background"])
    for drawing in data["drawings"]:
      self.draw(pyworld.assets.get_asset(drawing["image"]), drawing["position"], drawing["scale"], drawing["flip"])
    for gui in data["guis"]:
      self.gui(gui["id"], pyworld.assets.get_asset(gui["image"]), gui["position"], gui["scale"], gui["flip"])
    for text in data["texts"]:
      self.text(text["text"], text["color"], text["position"], text["scale"], text["flip"])
    pygame.display.update()
