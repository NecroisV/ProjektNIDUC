from enum import IntEnum

class FrameType(IntEnum):
    DATA = 1 #przesyłanie fragmentu pliku
    ACK = 2 #potwierdzenie odebrania ramki
    FIN = 3 #zakończenie transmisji

class Frame:
    def __init__(self, src,dst,frame_type,seq,data,crc=0):
        self.src = src  #Określa, kto wysyła ramkę
        self.dst = dst  #Określa, kto odbiera ramkę
        self.frame_type = frame_type  #Rozróżnia DATA, ACK, FIN
        self.seq = seq  #Numer ramki potrzebny do ACK i retransmisji
        self.data = data  #Przechowuje fragment pliku w bajtach
        self.crc = crc  #Przechowuje sumę kontrolną

    @property
    def length(self):
        return len(self.data)  #Automatycznie określa liczbę bajtów danych

    def to_bytes(self,detector):
        header_and_data = (
            self.src.to_bytes(1, "big")
            + self.dst.to_bytes(1, "big")
            + int(self.frame_type).to_bytes(1, "big")
            + self.seq.to_bytes(2, "big")
            + self.length.to_bytes(2, "big")
            + self.data
        )

        crc = detector.calculate(header_and_data)
        return header_and_data + crc
    
    
if __name__ == "__main__":
    frame = Frame(
        src=1,
        dst=2,
        frame_type=FrameType.DATA,
        seq=0,
        data=b"ABCD"
    )

    raw = frame.to_bytes()

    print("HEX:", raw.hex(" "))
    print("BIN:", " ".join(f"{byte:08b}" for byte in raw))
