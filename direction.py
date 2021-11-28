from enum import Enum

class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3
  NONE = 4


def to_direction(x, y):
  if x > 0:
    return Direction.RIGHT
  if x < 0:
    return Direction.LEFT
  if y < 0:
    return Direction.UP
  if y > 0:
    return Direction.DOWN
  return Direction.NONE
