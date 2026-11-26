from universal_calculations import calculate_division, create_frame


class Receiver:

  def __init__(
      self, divider, address, max_data_length, number_all_packages, chunk_size
  ):
    self.divider = divider
    self.address = address
    self.deg = divider.bit_length() - 1

    self.type_of_message = {"DATA": 0b111, "ACK": 0b110, "NCK": 0b100}
    self.max_data_length = max_data_length
    self.number_all_packages = number_all_packages
    self.chunk_size = chunk_size

    self.package_number = 1
    self.received_data = bytearray()

    # Statystyki ramek
    self.receive_calls = 0
    self.total_frames = 0
    self.bad_frames = 0
    self.none_frames = 0

  def reset_stats(self):
    self.receive_calls = 0
    self.total_frames = 0
    self.bad_frames = 0
    self.none_frames = 0

  def mean_bad_frames(self) -> float:
    if self.total_frames == 0:
      return 0.0
    return self.bad_frames / self.total_frames

  def mean_none_frames(self) -> float:
    if self.receive_calls == 0:
      return 0.0
    return self.none_frames / self.receive_calls

  def receive(self, message):
    self.receive_calls += 1

    if message is None:
      self.none_frames += 1
      return None

    self.total_frames += 1
    dummy_transmitter_address = 2**31 + 168
    data = 0
    data_length = 0

    if calculate_division(message, self.divider) == 0:
      frame = create_frame(
          self.type_of_message.get("ACK"),
          self.address,
          dummy_transmitter_address,
          self.number_all_packages,
          self.package_number,
          self.max_data_length,
          data_length,
          data,
          self.divider,
      )
      self.package_number = (self.package_number + 1) % (
          2**self.number_all_packages
      )
    else:
      self.bad_frames += 1
      frame = create_frame(
          self.type_of_message.get("NCK"),
          self.address,
          dummy_transmitter_address,
          self.number_all_packages,
          self.package_number,
          self.max_data_length,
          data_length,
          data,
          self.divider,
      )

    return frame