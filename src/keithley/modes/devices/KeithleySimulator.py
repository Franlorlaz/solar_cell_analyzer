"""Keithley Simulator for Debug."""

import time
from math import exp
from numpy import array


def list_voltage_hysteresis(v_1, v_2, points):
    """Generate a string with comma separated values.

    Two lists (string with comma separated values) are generated and
    merged. The first list is forward (from "v_1" to "v_2" with "points"
    number of points) and the second, backward (from "v_2" to "v_1" with
    another "points" points). This list allow execute a hysteresis
    measurement. The final length of the list is 2*points-1.

    :param v_1: Minimum voltage (float).
    :param v_2: Maximum voltage (float).
    :param points: Number of points of the forward/backward list.
    :return: A string with comma separated values.
    """
    step = (v_2 - v_1) / (points - 1)
    voltage = str(v_1)
    for j in range(1, points):
        voltage += ',' + str(v_1 + j * step)
    for j in range(1, points):
        voltage += ',' + str(v_1 + (points - 1 - j) * step)
    return voltage


class KeithleySimulator:
    """PyVISA class simulator for debug purposes"""

    @staticmethod
    def write(text):
        """Simulate `write()` method of a pyvisa object.

        Simulating: inst.write(text)

        :param text: Instruction to the instrument (str).
        :return: None
        """
        if len(text) >= 25:
            text = text[:25] + '...'
        print('KeithleySimulator:', text, sep=' ')

    @staticmethod
    def close():
        """Simulate `close()` method of a pyvisa object.

        Simulating: inst.close()
        """
        print('KeithleySimulator: close()')

    def query_ascii_values(self, text, container=None):
        """Simulate `query_ascii_values()` method of a pyvisa object.

        The `container` parameter must be a dictionary like:
        container = {'mode': <str>,
        'config': {'v_1': <float>, 'v_2': <float>, 'points': <int>,
        'speed': <float>, 'delay': <float>, 'cmpl': <float>}}

        :param text: Instruction to the instrument (str).
        :param container: A dict with information about the keithley program.
        :return: A `numpy.array` with data simulating a measurement (V, I, t).
        """
        KeithleySimulator.write(text)

        if container:
            if 'mode' not in container or 'config' not in container:
                raise ValueError(f'Unrecognized "container": '
                                 f'query_ascii_values({text}, '
                                 f'container={container})')
            v_1 = container['config']['v_1']
            v_2 = container['config']['v_2']
            points = container['config']['points']
        else:
            raise ValueError(f'Unrecognized "container": '
                             f'query_ascii_values({text}, '
                             f'container={container})')

        if container['mode'] == 'lineal':
            data = self.simulate_sweep_mode(v_1, v_2, points)
        elif container['mode'] == 'hysteresis':
            voltage = list_voltage_hysteresis(v_1, v_2, points)
            data = self.simulate_list_mode(voltage)
        else:
            raise ValueError(f'Unrecognized keithley mode in '
                             f'"container": query_ascii_values({text}, '
                             f'container={container})')
        time.sleep(5)
        return data

    @staticmethod
    def simulate_sweep_mode(v_1, v_2, points):
        """Simulate a measure with source in sweep mode.

        :param v_1: Start voltage (float).
        :param v_2: Stop voltage (float).
        :param points: Number of points for the list of voltages (int).
        :return: A `numpy.array` with data simulating a measurement (V, I, t).
        """
        step = (v_2 - v_1) / (points - 1)
        voltage = [v_1 + i*step for i in range(points)]
        voltage, current, t = KeithleySimulator.simulate_solar_cell(voltage)
        data = list(zip(voltage, current, t))
        return array(data)

    @staticmethod
    def simulate_list_mode(voltage):
        """Simulate a measure with source in list mode.

        :param voltage: String with comma separated values (str).
        :return: A `numpy.array` with data simulating a measurement (V, I, t).
        """
        voltage = voltage.split(',')
        voltage = [float(v) for v in voltage]
        voltage, current, t = KeithleySimulator.simulate_solar_cell(voltage)
        data = list(zip(voltage, current, t))
        return array(data)

    @staticmethod
    def simulate_solar_cell(voltage):
        """Simulate a solar cell IV curve with an exponential model.

        :param voltage: An iterable with voltages input.
        :return: Three lists. First with voltages, second with current and
        the last with timing (V, I, t).
        """
        current = []
        t = []
        for v in voltage:
            a = 1e-3
            b = 1.5
            c = -2e-3 - a
            i = a * exp(b*v) + c
            current.append(i)
            now = time.localtime()
            now = time.strftime('%H%M%S', now)
            t.append(int(now))
        return list(voltage), current, t
