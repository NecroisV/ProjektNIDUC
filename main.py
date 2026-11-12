import math
import random
from chanel import Channel
from receiever import Receiver
from transmiter import Transmitter

import matplotlib.pyplot as plt


invalid_frames = 0
all_frames = 0
file_name = "test.txt"
chunk_size = 32
max_data_length = int(math.log(chunk_size, 2))

transmitter_address = 0b11
receiver_address = 0b10

all_p = []
all_mean = []
p = 0.001

while p<=1:
  chanel = Channel(p)

  CRC_length = 4
  CRC_divider = random.randint(2 ** (CRC_length - 1), (2**CRC_length) - 1)


  transmitter = Transmitter(transmitter_address, chunk_size, CRC_divider, max_data_length)
  receiver = Receiver(CRC_divider)
  stat_list = []
  for i in range(10):
    invalid_frames = 0
    all_frames = 0
    for frame in transmitter.start_transmitting(file_name, receiver_address):
      sent_frame = chanel.send_data(frame)

      is_valid = receiver.verify_crc(sent_frame)
      if not is_valid:
        invalid_frames += 1
      all_frames += 1
    stat_list.append(invalid_frames/all_frames)
  print(f"{sum(stat_list)/len(stat_list)*100}% błędów przy CRC: {CRC_length} | P = {p}")
  all_p.append([p])
  all_mean.append(sum(stat_list)/len(stat_list)*100)
  p += 0.001


plt.plot(all_p, all_mean)
plt.show()
