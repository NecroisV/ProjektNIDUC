from enum import IntEnum
class FrameType(IntEnum):
    DATA = 1 #przesyłanie fragmentu pliku
    ACK = 2 #potwierdzenie odebrania ramki
    FIN = 3 #zakończenie transmisji

class Frame:
    def __init__(self, src,dst,frame_type,seq,data,crc=0):
        self.src = src  #Określa, kto wysyła ramkę
        self.dst = dst  #Określa, kto odbiera ramkę
        self.type = frame_type  #Rozróżnia DATA, ACK, FIN
        self.seq = seq  #Numer ramki potrzebny do ACK i retransmisji
        self.data = data  #Przechowuje fragment pliku w bajtach
        self.crc = crc  #Przechowuje sumę kontrolną

    @property
    def length(self):
        return len(self.data)  #Automatycznie określa liczbę bajtów danych

