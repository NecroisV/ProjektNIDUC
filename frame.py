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
    
    @classmethod
    def from_bytes(cls, raw: bytes, detector):

        crc_size = (detector.width + 7) // 8 

        if len(raw) < 7 + crc_size:
            raise ValueError("Ramka jest za krótka")

        data_without_crc = raw[:-crc_size]
        received_crc = raw[-crc_size:]

        if not detector.verify(data_without_crc, received_crc):
            raise ValueError("Niepoprawne CRC")

        src = raw[0]
        dst = raw[1]
        frame_type = FrameType(raw[2])
        seq = int.from_bytes(raw[3:5], "big")
        length = int.from_bytes(raw[5:7], "big")

        if length > 256:
            raise ValueError("Za duża długość DATA")

        data = raw[7:-crc_size]

        if len(data) != length:
            raise ValueError("Niepoprawna długość DATA")

        return cls(src, dst, frame_type, seq, data)
