import itertools
import random
from chanel import Channel
import matplotlib.pyplot as plt
import numpy as np
from receiever import Receiver
from transmiter import Transmitter

file_name = "test.txt"
chunk_size = 32  # 256 bitów
max_data_length = 9  # obsługuje długości do 511 bitów (mieści 256)
number_all_packages = 16

transmitter_address = 0b1110001001
receiver_address = 0b10110001101

# Listy wartości — każde z każdym
p_list = [0.0001, 0.0005]
p_b_list = [0.01, 0.05]
p_switch_list = [0, 0.005]

param_table = list(itertools.product(p_list, p_b_list, p_switch_list))
runs = 20

labels = []
mean_retx_list = []
mean_failed_list = []
mean_bad_rx_list = []

for p, p_b, p_switch_chance in param_table:
  CRC_length = 32
  CRC_divider = random.randint(2 ** (CRC_length - 1), (2**CRC_length) - 1)

  retx_runs = []
  failed_runs = []
  bad_rx_runs = []

  for _ in range(runs):
    receiver = Receiver(
        CRC_divider,
        receiver_address,
        max_data_length,
        number_all_packages,
        chunk_size,
    )
    chanel = Channel(p, p_b, [receiver], p_switch_chance)
    transmitter = Transmitter(
        transmitter_address,
        chunk_size,
        CRC_divider,
        max_data_length,
        chanel,
        number_all_packages,
    )

    transmitter.start_transmitting(file_name, receiver_address)

    retx_runs.append(transmitter.mean_retransmissions())
    failed_runs.append(transmitter.failed_frames)
    bad_rx_runs.append(receiver.mean_bad_frames())

  mean_retx = float(np.mean(retx_runs))
  mean_failed = float(np.mean(failed_runs))
  mean_bad_rx = float(np.mean(bad_rx_runs))

  label = f"p={p}\np_b={p_b}\nsw={p_switch_chance}"
  labels.append(label)
  mean_retx_list.append(mean_retx)
  mean_failed_list.append(mean_failed)
  mean_bad_rx_list.append(mean_bad_rx)

  print(
      f"p={p} | p_b={p_b} | p_switch={p_switch_chance} | "
      f"śr. retx={mean_retx:.3f} | "
      f"śr. nieudanych={mean_failed:.3f} | "
      f"śr. złych RX={mean_bad_rx:.3f}"
  )

x = np.arange(len(labels))
fig, axes = plt.subplots(4, 1, figsize=(max(10, len(labels) * 1.1), 12), sharex=True)

axes[0].plot(x, mean_retx_list, marker="o")
axes[0].set_ylabel("Śr. retransmisji")
axes[0].grid(True)

axes[1].plot(x, mean_failed_list, marker="s")
axes[1].set_ylabel("Śr. nieudanych")
axes[1].grid(True)

axes[2].plot(x, mean_bad_rx_list, marker="^")
axes[2].set_ylabel("Śr. złych RX")
axes[2].grid(True)

plt.tight_layout()
plt.show()