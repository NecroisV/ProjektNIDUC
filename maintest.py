from chanel import Channel
from receiever import Receiver
from arq.stop_and_wait import StopAndWait
from errror_detection.crc import CRC
from frame import Frame, FrameType


# Funkcja pomocnicza: pokazuje bajty jako zera i jedynki
def show_bits(raw):
    return " ".join(f"{byte:08b}" for byte in raw)


crc4 = CRC(4, 0b10011)
channel = Channel(error_chance=0.001)
receiver = Receiver(divider=0b10011)

stop_and_wait = StopAndWait(
    transmitter=None,
    receiver=receiver,
    channel=channel,
    detector=crc4
)


# Podgląd ramki przed wysłaniem
def show_frame(data):
    frame = Frame(
        src=1,
        dst=2,
        frame_type=FrameType.DATA,
        seq=stop_and_wait.seq,
        data=data
    )

    raw = frame.to_bytes(crc4)
    print("dane:", data)
    print("ramka szesntastkowa:", raw.hex(" "))
    print("ramka binarna:", show_bits(raw))
    print("długość danych:", frame.length)

print("\n------------- PIERWSZA RAMKA -------------")

show_frame(b"ABCD")
result = stop_and_wait.send(b"ABCD")
print("sukces:", result)

print("\n------------- DRUGA RAMKA -------------")

show_frame(b"EFGH")
result = stop_and_wait.send(b"EFGH")
print("sukces:", result)


print("\n------------- TRZECIA RAMKA -------------")

show_frame(b"IJKL")
result = stop_and_wait.send(b"IJKL")
print("sukces:", result)

