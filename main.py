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

transmitter_address = 0b11
receiver_address = 0b10

# Listy wartości — każde z każdym
p_list = [0.0001, 0.001, 0.01]
p_b_list = [0.01, 0.05]
p_switch_list = [0, 0.005, 0.02]

param_table = list(itertools.product(p_list, p_b_list, p_switch_list))
runs = 11

labels = []
mean_retx_list = []
mean_failed_list = []
mean_bad_rx_list = []
mean_none_rx_list = []
mean_none_tx_list = []

for p, p_b, p_switch_chance in param_table:
  CRC_length = 4
  CRC_divider = random.randint(2 ** (CRC_length - 1), (2**CRC_length) - 1)

  retx_runs = []
  failed_runs = []
  bad_rx_runs = []
  none_rx_runs = []
  none_tx_runs = []

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
    none_rx_runs.append(receiver.mean_none_frames())
    none_tx_runs.append(transmitter.mean_none_frames())

  mean_retx = float(np.mean(retx_runs))
  mean_failed = float(np.mean(failed_runs))
  mean_bad_rx = float(np.mean(bad_rx_runs))
  mean_none_rx = float(np.mean(none_rx_runs))
  mean_none_tx = float(np.mean(none_tx_runs))

  label = f"p={p}\np_b={p_b}\nsw={p_switch_chance}"
  labels.append(label)
  mean_retx_list.append(mean_retx)
  mean_failed_list.append(mean_failed)
  mean_bad_rx_list.append(mean_bad_rx)
  mean_none_rx_list.append(mean_none_rx)
  mean_none_tx_list.append(mean_none_tx)

  print(
      f"p={p} | p_b={p_b} | p_switch={p_switch_chance} | "
      f"śr. retx={mean_retx:.3f} | "
      f"śr. nieudanych={mean_failed:.3f} | "
      f"śr. złych RX={mean_bad_rx:.3f} | "
      f"śr. None RX={mean_none_rx:.4f} | "
      f"śr. None TX={mean_none_tx:.4f}"
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

axes[3].plot(x, mean_none_rx_list, marker="d", label="None w RX")
axes[3].plot(x, mean_none_tx_list, marker="x", label="None w TX")
axes[3].set_ylabel("Śr. ramek None")
axes[3].set_xticks(x)
axes[3].set_xticklabels(labels, rotation=45, ha="right")
axes[3].legend()
axes[3].grid(True)

plt.tight_layout()
plt.show()