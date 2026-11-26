import random


class Channel:
  def __init__(self, error_chance):
    self.error_chance = error_chance

  def send_data(self, raw: bytes) -> bytes:
    corrupted = bytearray(raw)
    for i in range(len(corrupted)):
            for bit in range(8):
                if random.random() < self.error_chance:
                    corrupted[i] ^= (1 << bit)

    return bytes(corrupted)