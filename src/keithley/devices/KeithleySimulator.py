
# TODO: keithley_virtual

from pathlib import Path
from numpy import loadtxt


class KeithleySimulator:

    def __init__(self):
        self.lineal = Path(__file__ + '/../../../config/debug/02_B.txt')
        self.hysteresis = Path(__file__ + '/../../../config/debug/hyster.txt')

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

    def query_ascii_values(self, text, container='lineal'):
        # TODO: extract data from file and return it in a np.array
        KeithleySimulator.write(text)

        if container == 'lineal':
            file = str(self.lineal.resolve())
            data = loadtxt(file, skiprows=3)
        elif container == 'hysteresis':
            file = str(self.hysteresis.resolve())
            data = loadtxt(file, skiprows=2)
        else:
            raise ValueError(f'Unrecognized keithley mode in '
                             f'"container": query_ascii_values({text}, '
                             f'container={container})')
        return data

    def simulate_sweep_mode(self, v_1, v_2, points):
        pass

    def simulate_list_mode(self, voltage, points):
        pass

    @staticmethod
    def simulate_solar_cell(voltage):
        v2 = max(voltage)
        i1 = -1
        i2 = 1
        current = []
        for v in voltage:
            current.append((i2-i1)**(v/v2)+i1)
        return voltage, current
