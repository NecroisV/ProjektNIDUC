from universal_calculations import calculate_division


class Reciever:

  def __init__(self, divider: int):
    # Store the divider so the receiver knows the CRC standard
    self.divider = divider

  def verify_crc(self, received_message: int) -> bool:
    """Verifies a received frame using the stored divider."""
    return calculate_division(received_message, self.divider) == 0