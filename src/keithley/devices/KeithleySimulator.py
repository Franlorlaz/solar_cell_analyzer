
# TODO: keithley_virtual


class KeithleySimulator:

    @staticmethod
    def write(text):
        if len(text) >= 25:
            text = text[:25] + '...'
        print('KeithleySimulator:', text, sep=' ')

    @staticmethod
    def measure_simulation():
        pass

    @staticmethod
    def close():
        """Simulate close method of a pyvisa object.

        Simulating: inst.close()
        """
        print('KeithleySimulator: close()')

    def query_ascii_values(self, text, **kwargs):
        # TODO: extract data from file and return it in a np.array
        pass
