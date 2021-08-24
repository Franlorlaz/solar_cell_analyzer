"""ESP32 Simulator for Debug."""


class ESP32Simulator:
    """Serial class simulator for debug purposes."""

    @staticmethod
    def write(text):
        """Simulate write method of a serial object.

        Simulating `ser` behaviour: ser.write(text)
        """
        print('ESP32Simulator:', text, sep=' ')

    @staticmethod
    def close():
        """Simulate close method of a serial object.

        Simulating `ser` behaviour: ser.close()
        """
        print('ESP32Simulator: close()')
