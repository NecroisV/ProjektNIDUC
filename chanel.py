import random


class Channel:
  def __init__(self, error_chance: float):
    self.error_chance = error_chance

  def send_data(self, frame: int) -> int:
    for i in range(frame.bit_length()):
      if random.random() < self.error_chance:
        frame ^= 1 << i
    return frame