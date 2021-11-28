from pyworld.game import Game
from pyworld.io import IO
from pyworld.locals import *
from pygame.locals import *
from horsey import Horsey
from puff import Puff
from tilemap import Tilemap
from copy import deepcopy
from time import time
from state import State
from controls import Controls, button
from pyworld.key import Key
from maker import Maker
from start import Start
from timer import Timer
import json
import tkinter as tk
from pygame.event import Event
from math import floor


class Play:
  def __init__(self):
    self.game = Game()

    self.level = Tilemap(self.game)
    self.level.init_tiles = False

    self.tilemap = Tilemap(self.game)
    self.player_start = (0, -2)
    self.show_win = 0

    self.player_types = [Puff, Horsey]
    self.player_index = 0
    self.player_type = self.player_types[self.player_index]
    self.player = self.player_type(self.game, self.tilemap)
    self.setup_level = True

    self.switch_mode = Key(self.game, button(Controls.EDITOR))
    self.switch_char_button = Key(self.game, button(Controls.SWITCH))
    self.add_time = Key(self.game, button(Controls.ADD))
    self.remove_time = Key(self.game, button(Controls.REMOVE))
    self.game_state = State.MAKE

    self.maker = Maker(self.game, self.level)

    self.game.on(PRESS, self.press)
    self.game.on(FINISH, self.finish)

    self.timer = Timer()
  
  def press(self, evt):
    if evt.gui == "menu":
      self.menu(self)
    elif evt.gui == "player":
      self.switch_char()
  
  def switch_char(self):
    x = self.player.x
    y = self.player.y
    if self.player.grounded or self.game_state == State.MAKE:
      y -= 0.2
    xv = self.player.xv
    yv = self.player.yv
    self.player_index += 1
    self.player_index %= len(self.player_types)
    self.player_type = self.player_types[self.player_index]
    self.start_level(False)
    self.player.x = x
    self.player.y = y
    self.player.xv = xv
    self.player.yv = yv

  def finish(self, evt):
    self.show_win = time() + 1
    self.switch_state(State.MAKE)

  def start_level(self, reset_world=True):
    if reset_world:
      self.setup_level = True
      self.tilemap.snoap = []
      self.tilemap.tiles = deepcopy(self.level.tiles)
      self.tilemap.init_all_tiles()
      for coord, tile in self.tilemap.tiles.items():
        if isinstance(tile, Start):
          self.player_start = coord
    self.player = self.player_type(self.game, self.tilemap)

  def tick(self, event):
    self.game.background((36, 227, 217))
    if self.game_state == State.PLAY:
      self.player.tick()
      self.tilemap.render()
    elif self.game_state == State.MAKE:
      self.level.render()
      self.maker.tick()
    if self.setup_level:
      self.timer.reset()
      self.player.x = self.player_start[0]
      self.player.y = self.player_start[1]
      self.setup_level = False
    
    if self.switch_mode.just_down:
      if self.game_state == State.MAKE:
        self.switch_state(State.PLAY)
      else:
        self.switch_state(State.MAKE)
    
    if self.switch_char_button.just_down:
      self.switch_char()
    
    self.game.gui("menu", "menu_bar", 0.9, 0.1)

    if self.show_win > time():
      self.game.gui("win", "you_win", 0.5, 0.5, 2)
    
    if self.timer.die():
      self.tilemap.event(Event(HURT))
    
    if self.game_state == State.MAKE:
      if self.add_time.just_down:
        self.timer.add()
      if self.remove_time.just_down:
        self.timer.remove()
    
    self.game.gui("player", self.player.sprite, 0.9, 0.9, 0.75)
    self.game.text(str(floor(self.timer.render())), (255, 255, 255), 0.9, 0.3)

  def switch_state(self, new_state):
    self.game_state = new_state
    if new_state == State.PLAY:
      self.maker.active = False
      self.start_level()
      self.timer.start()
    elif new_state == State.MAKE:
      self.maker.active = True
      self.timer.stop()

  def hurt(self, event):
    self.start_level()

  def start(self):
    self.game.title = "Make the Jump 2!"
    self.game.io = IO(self.game)

    self.switch_state(State.MAKE)

    self.game.cam["size"] = 8
    self.game.on(TICK, self.tick)
    self.tilemap.on(HURT, self.hurt)

    self.game.start()
  
  def to_json(self):
    level = {"blocks": [], "timer": self.timer.time_len}
    for coord, tile in self.level.tiles.items():
      level["blocks"].append([[coord[0], coord[1]], tile.render()])
    
    return json.dumps(level)
  
  def from_json(self, level_json):
    new_tiles = {}
    level = json.loads(json.loads(level_json)["data"])
    self.timer.time_len = level["timer"]
    for pos_tile in level["blocks"]:
      pos = tuple(pos_tile[0])
      tile = pos_tile[1]

      for material in self.maker.example_materials:
        if material[0] == tile:
          new_tiles[pos] = material[1]()
    self.level.tiles = new_tiles
