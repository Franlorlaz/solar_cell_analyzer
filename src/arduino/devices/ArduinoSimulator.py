"""Arduino Simulator for Debug."""


class ArduinoSimulator:
    """Serial class simulator for debug purposes."""

    @staticmethod
    def write(text):
        """Simulate write method of a serial object.

        Simulating `ser` behaviour: ser.write(text)
        """
        print('ArduinoSimulator:', text, sep=' ')

    @staticmethod
    def close():
        """Simulate close method of a serial object.

        Simulating `ser` behaviour: ser.close()
        """
        print('ArduinoSimulator: close()')
