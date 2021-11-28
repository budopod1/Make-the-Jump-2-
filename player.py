from physics import Physics
from pyworld.key import Key
from controls import Controls, button


class Player(Physics):
  def __init__(self, game, tilemap):
    self.jump_power = 4
    self.move_speed = 3
    self.ground_pound = 5
    self.ground_pounding = False
    self.wrong_speed_reduction = 1
    self.ground_friction = 3
    super().__init__(game, tilemap)
    self.jump = Key(game, button(Controls.UP))
    self.left = Key(game, button(Controls.LEFT))
    self.right = Key(game, button(Controls.RIGHT))
    self.down = Key(game, button(Controls.DOWN))
    self.sprite = "eraser"

  def tick(self):
    super().tick()
    if self.active:
      self.game.cam["x"] = self.x
      self.game.cam["y"] = self.y

      if self.jump.down and self.grounded:
        self.yv -= self.jump_power
      
      speed = abs(self.xv)
      if speed < 1:
        speed = 1

      wrong_speed_reduction = 1 - self.wrong_speed_reduction * self.game.time_delta

      if self.left.down:
        self.reverse = True
        if self.xv > 0:
          self.xv *= wrong_speed_reduction
        self.xv -= self.move_speed / speed * self.game.time_delta

      elif self.right.down:
        self.reverse = False
        if self.xv < 0:
          self.xv *= wrong_speed_reduction
        self.xv += self.move_speed / speed * self.game.time_delta
      
      elif self.grounded:
        self.xv *= 1 - self.ground_friction * self.game.time_delta
      
      if (self.down.just_down or self.grounded) and self.ground_pounding:
        self.ground_pounding = False
        self.xv = 0
        self.yv = 0
      
      if self.down.just_down and not self.ground_pounding:
        self.ground_pounding = True
        self.xv = 0
      
      if self.ground_pounding:
        self.yv = self.ground_pound

      self.game.draw(self.sprite, self.x, self.y, 1, self.reverse)
