from frame import Frame, FrameType


class Receiver:
    def __init__(self, divider):
        self.divider = divider

    def receive(self, raw: bytes, detector):
        try:
            frame = Frame.from_bytes(raw, detector)
        except ValueError:
            return None

        if frame.frame_type != FrameType.DATA:
            return None

        print("Odbiornik otrzymał:", frame.data)

        ack = Frame(
            src=frame.dst,
            dst=frame.src,
            frame_type=FrameType.ACK,
            seq=frame.seq,
            data=b""
        )

        return ack.to_bytes(detector)