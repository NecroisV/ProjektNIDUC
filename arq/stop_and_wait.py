from frame import Frame, FrameType

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

        raw = frame.to_bytes(self.detector)

        received_raw = self.channel.send_data(raw)

        return received_raw