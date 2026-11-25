from universal_calculations import calculate_division

class CRC:
    def __init__(self, width, polynomial):
        self.width = width  #Liczba bitów CRC, np. 4 albo 32
        self.polynomial = polynomial  #Wielomian wykorzystywany do obliczania CRC

        if polynomial.bit_length() != width + 1:
            raise ValueError("Niepoprawny stopień wielomianu")

    def calculate(self, data: bytes) -> bytes: #przyjmuje i wzraca bajty
        # Zamiana bajtów na liczbę
        data_int = int.from_bytes(data, "big")

        # Dopisanie zer do obliczenia CRC
        padded_data = data_int << self.width

        # Dzielenie wielomianowe
        remainder = calculate_division(padded_data,self.polynomial)

        # Zamiana CRC na bajty
        crc_size = (self.width + 7) // 8
        return remainder.to_bytes(crc_size, "big")
    def verify(self, data: bytes, received_crc: bytes) -> bool:
        calculated_crc = self.calculate(data)
        return calculated_crc == received_crc


if __name__ == "__main__":
    crc4 = CRC(4, 0b10011)

    data = b"ABCD"

    result = crc4.calculate(data)
    print("data:", data.hex(" "))
    print("HEX:", result.hex(" "))
    print("BIN:", f"{result[0]:08b}")

    checksum = crc4.calculate(data)

    print(crc4.verify(data, checksum))     # True
    print(crc4.verify(b"ABXD", checksum))  # False
    

    