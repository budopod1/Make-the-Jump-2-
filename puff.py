from player import Player


class Puff(Player):
  def __init__(self, game, tilemap):
    super().__init__(game, tilemap)

    self.hit_points = [
      (0, -0.5),
      (0, -0.4)
    ]

    self.sprite = "puff"
    