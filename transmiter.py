from universal_calculations import calculate_division


def calculate_crc(data, divider):
    #Calculates the CRC remainder for the sender
    padded_data = data << divider.bit_length() - 1

    rest = calculate_division(padded_data, divider)
    return rest


class Transmitter:
    def __init__(self, address, chunk_size, divider, max_data_length):
        self.address = address
        self.chunk_size = chunk_size
        self.divider = divider
        self.max_data_length = max_data_length

        # State tracking
        self.package_number = 1
        self.file = None

        self.number_all_packages = 16 #it is 2^16 but for convenience it is saved as 16
        self.deg = divider.bit_length() - 1

    def open_file(self, filename):
        #Opens (or re-opens) the file from the very beginning.
        if self.file:
            self.file.close()
        self.file = open(filename, "rb")
        self.package_number = 1  # Reset package counter on fresh open

    def start_transmitting(self, file_name, receiver_address):
        self.file = None
        prepared_frame = self.get_next_frame(file_name, receiver_address)
        while prepared_frame:
            yield prepared_frame
            prepared_frame = self.get_next_frame(file_name, receiver_address)

    def get_next_frame(self, file_name, receiver_address) -> int | None:
        """Reads the next chunk, builds the frame, and returns it.

        Returns None when the end of the file is reached.
        """
        if self.file is None:
            self.open_file(file_name)

        # Read a single chunk from the current file position
        chunk = self.file.read(self.chunk_size)
        if not chunk:
            # End of file reached; close the handle
            self.file.close()
            self.file = None
            return None

        # Process data and pack
        data = int.from_bytes(chunk, byteorder="big")
        data_length = data.bit_length()

        sending_data = int(receiver_address) << 2 | self.address
        sending_data = sending_data << self.number_all_packages | self.package_number
        sending_data = sending_data << self.max_data_length | data_length
        sending_data = sending_data << data_length | data

        # Calculate CRC and build frame
        crc = calculate_crc(sending_data, self.divider)
        frame = (sending_data << self.deg) | crc

        # Increment package number for the next frame
        self.package_number = (self.package_number + 1) % (
                2 ** self.number_all_packages
        )

        return frame

