from universal_calculations import calculate_division, create_frame


class Transmitter:

  def __init__(
      self,
      transmitter_address,
      chunk_size,
      divider,
      max_data_length,
      chanel,
      number_all_packages,
  ):
    self.transmitter_address = transmitter_address
    self.chunk_size = chunk_size
    self.divider = divider
    self.max_data_length = max_data_length
    self.chanel = chanel

    # State tracking
    self.package_number = 1
    self.file = None

    self.number_all_packages = number_all_packages

    self.max_retransmissions = 10
    self.type_of_message = {"DATA": 0b111, "ACK": 0b110, "NCK": 0b100}

    # Statystyki transmisji
    self.total_retransmissions = 0
    self.frames_attempted = 0
    self.failed_frames = 0
    self.send_calls = 0

  def reset_stats(self):
    self.total_retransmissions = 0
    self.frames_attempted = 0
    self.failed_frames = 0
    self.send_calls = 0

  def mean_retransmissions(self) -> float:
    if self.frames_attempted == 0:
      return 0.0
    return self.total_retransmissions / self.frames_attempted


  def check_ack(self, message, type_bits=3):
    if message is None:
      return False
    if calculate_division(message, self.divider) != 0:
      return False
    if message.bit_length() < type_bits:
      return False

    msg_type = message >> (message.bit_length() - type_bits)
    return msg_type == self.type_of_message.get("ACK")


  def open_file(self, filename):
    if self.file:
      self.file.close()
    self.file = open(filename, "rb")
    self.package_number = 1


  def _send_once(self, frame: int) -> int | None:
    self.send_calls += 1
    response = self.chanel.send_data(frame)
    return response


  def start_transmitting(self, file_name, receiver_address):
    self.file = None
    prepared_frame = self.get_next_frame(file_name, receiver_address)

    while prepared_frame is not None:
      self.frames_attempted += 1
      retransmissions = 0
      got_ack = False

      while retransmissions <= self.max_retransmissions:
        got_ack = self.check_ack(self._send_once(prepared_frame))
        if got_ack:
          break
        retransmissions += 1
        self.total_retransmissions += 1

      if not got_ack:
        self.failed_frames += 1

      prepared_frame = self.get_next_frame(file_name, receiver_address)

  def get_next_frame(self, file_name, receiver_address) -> int | None:
    if self.file is None:
      self.open_file(file_name)

    chunk = self.file.read(self.chunk_size)
    if not chunk:
      self.file.close()
      self.file = None
      return None

    data = int.from_bytes(chunk, byteorder="big")
    data_length = data.bit_length()

    frame = create_frame(
        self.type_of_message.get("DATA"),
        self.transmitter_address,
        receiver_address,
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

    return frame