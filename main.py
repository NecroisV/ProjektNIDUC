import random

def calculate_division(data, divider):
    data_len = data.bit_length()
    for i in range(data_len - divider.bit_length(), -1, -1):
        if (data >> (divider.bit_length() - 1 + i)) & 1:
            data ^= divider << i
    return data

def calculate_crc(data: int, divider: int) -> int:
    #Calculates the CRC remainder for the sender
    padded_data = data << divider.bit_length() - 1

    rest = calculate_division(padded_data, divider)
    return rest

def verify_crc(received_message: int, divider: int) -> bool:
    #Verifies a received frame
    return calculate_division(received_message, divider) == 0


CRC_length = 32
CRC_divider = random.randint(2 ** (CRC_length - 1), (2**CRC_length) - 1)
print(f"Random CRC Divider:  {bin(CRC_divider)}")

address = 0b1

package_number = 0b1
number_all_packages = 32

data = 0b1000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111100001111000011110000111
data_length = data.bit_length()
data_length_length = 16

print(f"Original Data:       {bin(data)}")

sending_data = address << number_all_packages | package_number
sending_data = sending_data << data_length_length | data_length
sending_data = sending_data << data_length | data

print(f"Sending Data:       {bin(sending_data)}")
deg = CRC_divider.bit_length() - 1
crc = calculate_crc(sending_data, CRC_divider)
print(f"Calculated CRC:      {bin(crc)}")

transmitted_frame = (sending_data << deg) | crc
print(f"Transmitted Frame:   {bin(transmitted_frame)}")
print("-" * 40)

print(f"Receiver checks clean frame:    Valid? {verify_crc(transmitted_frame, CRC_divider)}")
