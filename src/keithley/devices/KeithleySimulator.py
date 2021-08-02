
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
