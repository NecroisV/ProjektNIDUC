from frame import Frame, FrameType
#BRAKUJE JESZCZE:
#PONOWNEGO WYSYLANIA DANYCH
#OBSUŁGI TIMEAUTOW
#JESZCZE PARU RZECZY PEWNIE
class StopAndWait:
    def __init__(self, transmitter, receiver, channel, detector):
        self.transmitter = transmitter
        self.receiver = receiver
        self.channel = channel
        self.detector = detector
        self.seq = 0

    def send(self, data: bytes):
        frame = Frame(
            src=1,
            dst=2,
            frame_type=FrameType.DATA,
            seq=self.seq,
            data=data
        )

        # Tworzymy bajty ramki DATA
        raw = frame.to_bytes(self.detector)

        # Wysyłamy DATA przez kanał BSC
        received_raw = self.channel.send_data(raw)

        # Odbiornik sprawdza DATA i tworzy ACK
        ack_raw = self.receiver.receive(received_raw,self.detector)

        # Jeśli DATA była uszkodzona, ACK nie powstał
        if ack_raw is None:
            print("Brak ACK")
            return False

        # ACK również przechodzi przez kanał
        received_ack_raw = self.channel.send_data(ack_raw)

        # Nadajnik sprawdza otrzymane ACK
        try:
            ack = Frame.from_bytes(received_ack_raw,self.detector)
        except ValueError:
            print("Uszkodzone ACK")
            return False

        # Sprawdzamy, czy ACK potwierdza właściwą ramkę
        if ack.frame_type != FrameType.ACK or ack.seq != self.seq:
            print("Nieprawidłowe ACK")
            return False

        print("Otrzymano ACK dla SEQ =", self.seq)

        # Przechodzimy do kolejnego numeru ramki
        self.seq = (self.seq + 1) % 2

        return True
    