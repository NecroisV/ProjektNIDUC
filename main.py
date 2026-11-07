import math
import random
from chanel import Channel
from reciever import Reciever
from transmiter import Transmitter

transmitter_address = 0b11
receiver_address = 0b10

chanel = Channel(0.001)

CRC_length = 3
CRC_divider = random.randint(2 ** (CRC_length - 1), (2**CRC_length) - 1)

chunk_size = 128
max_data_length = int(math.log(chunk_size, 2))

file_name = "test.txt"
transmitter = Transmitter(
    transmitter_address, chunk_size, CRC_divider, max_data_length
)
receiver = Reciever(CRC_divider)

# Use a standard 'for' loop to iterate through every yielded frame naturally
for frame in transmitter.start_transmitting(file_name, receiver_address):
  # Send frame through the noisy channel
  sent_frame = chanel.send_data(frame)
  print(bin(sent_frame))

  # Check if the receiver validates it successfully
  is_valid = receiver.verify_crc(sent_frame)
  print(f"Frame received & verified: {is_valid}")