from enum import Enum
from pygame.locals import *


class Controls(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3
  EDITOR = 4
  SWITCH = 5
  ADD = 6
  REMOVE = 7


key_map = {Controls.UP: K_w, Controls.DOWN: K_s, Controls.LEFT: K_a, Controls.RIGHT: K_d, Controls.EDITOR: K_e, Controls.SWITCH: K_q, Controls.ADD: KSCAN_F4, Controls.REMOVE: K_MINUS}

def button(control):
  return key_map[control]
