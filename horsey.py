from player import Player


class Horsey(Player):
  def __init__(self, game, tilemap):
    super().__init__(game, tilemap)

    self.hit_points = [
      (-0.37, -0.42),
      (0.11,-0.09),
      (0.38, -0.07),
      (0.49,0.02),
      (0.26,0.19),
      (0.05,0.4),
      (-0.05,0.4),
      (-0.22,0.16),
      (-0.37,-0.06),
      (0.07,-0.42)
    ]

    self.sprite = "horsey"
    