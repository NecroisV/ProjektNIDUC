def calculate_division(data, divider):
    data_len = data.bit_length()
    for i in range(data_len - divider.bit_length(), -1, -1):
        if (data >> (divider.bit_length() - 1 + i)) & 1:
            data ^= divider << i
    return data

def calculate_crc(data, divider):
    #Calculates the CRC remainder for the sender
    padded_data = data << divider.bit_length() - 1

    rest = calculate_division(padded_data, divider)
    return rest

def create_frame(type_of_message,
                 transmitter_address, receiver_address,
                 number_all_packages, package_number,
                 max_data_length, data_length, data, divider):
    deg = divider.bit_length() - 1

    sending_data = type_of_message << 32 | transmitter_address
    sending_data = sending_data << 32 | receiver_address
    sending_data = sending_data << number_all_packages | package_number
    sending_data = sending_data << max_data_length | data_length
    sending_data = sending_data << data_length | data

    # Calculate CRC and build frame
    crc = calculate_crc(sending_data, divider)
    frame = (sending_data << deg) | crc

    return frame