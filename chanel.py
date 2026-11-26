import random


class Channel:
  def __init__(self, error_chance_good, error_chance_bad, receiver_list, switch_channels_chance):
        self.error_chance = error_chance_good
        self.error_chance_good = error_chance_good
        self.error_chance_bad = error_chance_bad
        self.receiver_list = receiver_list
        self.package_lose_chance = 0.0000000001
        self.switch_channels_chance = switch_channels_chance


  def corrupt_data(self, message: int | None) -> int | None:
      if message is None:
          return None

      if random.random() < self.package_lose_chance:
          return None

      bit_len = message.bit_length()
      for bit in range(bit_len):
          if random.random() < self.error_chance:
              message ^= 1 << bit
          if random.random() < self.switch_channels_chance:
              if self.error_chance == self.error_chance_good:
                  self.error_chance = self.error_chance_bad
              else:
                  self.error_chance = self.error_chance_good
      return message

  def send_data(self, message):
    corrupted = self.corrupt_data(message)
    for receiver in self.receiver_list:
        return_message = receiver.receive(corrupted)
        if return_message is not None:
            return self.corrupt_data(return_message)
        else:
            return None
    return None
