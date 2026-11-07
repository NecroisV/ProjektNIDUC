def calculate_division(data, divider):
    data_len = data.bit_length()
    for i in range(data_len - divider.bit_length(), -1, -1):
        if (data >> (divider.bit_length() - 1 + i)) & 1:
            data ^= divider << i
    return data