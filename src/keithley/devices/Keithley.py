"""Keithley Main Class Definition.

Common port: 'GPIB0::24::INSTR'

Recommended order for programming the keithley:

keithley.set_config(config)
keithley.set_sensors()
keithley.set_source()

## choose one:
keithley.source_sweep_mode()
keithley.source_list_mode()
##

keithley.set_trigger()
keithley.set_display()
keithley.run()
keithley.save(file)
"""

import numpy as np
import pyvisa as visa
from pathlib import Path

from .KeithleySimulator import KeithleySimulator


class Keithley:

    def __init__(self, port=None, v_1=1.2, v_2=-0.1, points=200,
                 speed=0.240, delay=0.001, cmpl=0.05, **kwargs):
        """Initialize Keithley object."""
        self.port = port
        self.inst = self.open_resource(port=port)

        self.v_1 = float(v_1)
        self.v_2 = float(v_2)
        self.points = int(points)
        self.speed = float(speed)
        self.delay = float(delay)
        self.cmpl = float(cmpl)

        self._data_length = points
        self._data = None

    @staticmethod
    def search_ports():
        """List all available ports.

        This function obtain a tuple of strings with the ports available
        to connect.

        :return: A tuple of available resources (strings).
        """
        return visa.ResourceManager().list_resources()

    def open_resource(self, port, close_before=False):
        """Connect to the indicated port.

        :param port: A string with the port to connect (resource).
        :param close_before: Disconnect or not (boolean) the current
        device before connecting to the new one.
        :return: A pyserial object.
        """
        if close_before:
            self.close_resource()

        if port:
            self.inst = visa.ResourceManager().open_resource(port)
            self.inst.timeout = 1e8
            # self.inst.write(':TRAC:CLE')      # Clear the buffer of readings
            self.inst.write('*RST')           # Reset unit to GPIB defaults
            self.inst.write(':SYST:RSEN ON')  # 4-wire remote sensing
        else:
            self.inst = KeithleySimulator()

        self.port = port
        print('Keithley connected to: ', port)
        return self.inst

    def close_resource(self):
        """Disconnect keithley and connect to KeithleySimulator.

        :return: A pyvisa object.
        """
        self.inst.close()
        self.port = None
        self.inst = KeithleySimulator()
        print('Keithley disconnected')
        return self.inst

    def set_config(self, config, data_length=None):
        """Set keithley configuration.

        :param config: A dictionary with this structure:
        {"v_1": 1.2, "v_2": -0.1, "points": 200, "speed": 0.240,
        "delay": 0.001, "cmpl": 0.05, "light_power": 1.0, "area": 0.14}
        :param data_length: Specify the data length (int, optional).
        :return: None
        """
        self.v_1 = float(config['v_1'])
        self.v_2 = float(config['v_2'])
        self.points = int(config['points'])
        self.speed = float(config['speed'])
        self.delay = float(config['delay'])
        self.cmpl = float(config['cmpl'])

        self._data_length = self.points
        if data_length:
            self._data_length = data_length

    def set_sensors(self, cmpl=None):
        """Sensors configuration.

        :param cmpl: Compliance (optional, float).
        :return: None
        """
        inst = self.inst
        if not cmpl:
            cmpl = self.cmpl

        inst.write(':SENS:FUNC "CURR","VOLT"')  # Enable sense functions
        inst.write(':SENS:RES:MODE MAN')  # Manual resistance mode
        inst.write(':SENS:CURR:PROT %f' % cmpl)  # set the current compliance
        inst.write(':SENS:CURR:RANG 1E-3')  # current range
        inst.write(':SENS:CURR:RANG:AUTO ON')  # disable current auto range
        # inst.write(':SENS:VOLT:RANG 1')          # voltage range (measure)
        # inst.write(':SENS:VOLT:RANG:AUTO OFF')   # disable voltage auto range
        inst.write(':SENS:CURR:NPLC 1')  # curr measure speed (PowerLineCycles)
        inst.write(':SENS:VOLT:NPLC 1')  # volt measure speed (PowerLineCycles)

    def set_source(self, delay=None):
        """Source configuration.

        :param delay: Delay (optional, float).
        :return: None
        """
        inst = self.inst
        if not delay:
            delay = self.delay

        inst.write(':SOUR:FUNC VOLT')  # volts source function
        inst.write(':SOUR:VOLT:PROT 20')  # V-source protection
        inst.write(':SOUR:DEL %f' % delay)  # source-delay-measure MANUAL
        # inst.write(':SOUR:DEL:AUTO ON')     # source-delay-measure AUTO
        inst.write(':SOUR:VOLT:RANG 1')  # voltage range (source)
        inst.write(':SOUR:VOLT:RANG:AUTO ON')  # disable voltage auto range

    def set_trigger(self, points=None, speed=None):
        """Trigger configuration.

        :param points: Number of points (optional, integer).
        :param speed: Trigger delay (optional, float).
        :return: None
        """
        inst = self.inst
        if not points:
            points = self._data_length
        if not speed:
            speed = self.speed

        inst.write(':TRIG:COUN %f' % points)  # Trigger count
        inst.write(':TRIG:DEL %f' % speed)  # Trigger delay

    def set_display(self):
        """Display configuration."""
        inst = self.inst
        inst.write(':DISP:WIND:TEXT:STAT OFF')  # display state
        inst.write(':DISP:WIND:TEXT:DATA "hello world"')  # display message
        inst.write(':DISP:CND')  # Return to source-measure display state

    def run(self):
        """Run keithley program, read data and finish.

        :return: A numpy array with data measured (V, I, t).
        """
        inst = self.inst
        points = self._data_length

        # inst.write(':TRAC:TST:FORM DELT')  # timestamp format: ABSolute/DELTa
        inst.write(':FORM:ELEM VOLT,CURR,TIME')  # query elements in data
        inst.write(':OUTP ON')  # open output
        data = inst.query_ascii_values(':READ?', container=np.array)
        # inst.query(':TRAC:TST:FORM?')  # read timestamp format
        # inst.query(':SYST:TIME?')      # returns the current timestamp value
        inst.write(':OUTP OFF')  # close output

        self._data = np.reshape(data, (points, 3))
        return self._data

    def source_sweep_mode(self, v_1=None, v_2=None, points=None):
        """Configure source in sweep mode.

        :param v_1: Start voltage (float, optional).
        :param v_2: Stop voltage (float, optional).
        :param points: Number of points for the sweep (integer, optional).
        :return: None
        """

        inst = self.inst
        if not v_1:
            v_1 = self.v_1
        if not v_2:
            v_2 = self.v_2
        if not points:
            points = self.points
            self._data_length = points

        inst.write(':SOUR:SWE:SPAC LIN')          # Linear sweep
        inst.write(':SOUR:VOLT:STAR %f' % v_1)    # start voltage
        inst.write(':SOUR:VOLT:STOP %f' % v_2)    # stop voltage
        inst.write(':SOUR:SWE:POIN %f' % points)  # Sweep points

    def source_list_mode(self, voltage=None, points=None):
        """Configure source in list mode.

        :param voltage: String with comma separated values (str, optional).
        The instrument read this string like a list of voltage to set the
        source.
        :param points: Number of points passed in "voltage" (int, optional).
        :return: None
        """

        inst = self.inst
        if not points:
            points = 2 * self.points - 1
            self._data_length = points
        if not voltage:
            voltage = Keithley._list_voltage_hysteresis(self.v_1, self.v_2,
                                                        points)

        inst.write(':SOUR:VOLT:MODE LIST')           # Volts list mode
        inst.write(':SOUR:LIST:VOLT %s' % voltage)   # Volts list
        # inst.write(':SOUR:LIST:POIN %f' % points)  # Sweep points

    @staticmethod
    def _list_voltage_hysteresis(v_1, v_2, points):
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

    def save(self, file_name, data=None, data_length=None, config=None):
        """Save data in a file.

        :param file_name: Path to file where to save data (str or Path object).
        :param data: A numpy array with data measured (V, I, t).
        :param data_length: Specify the data length (int).
        :param config: A dictionary with this structure:
        {"v_1": 1.2, "v_2": -0.1, "points": 200, "speed": 0.240,
        "delay": 0.001, "cmpl": 0.05, "light_power": 1.0, "area": 0.14}
        :return: None
        """
        file_name = Path(file_name)

        if not data:
            data = self._data
        if not data_length:
            data_length = self._data_length
        if config:
            self.set_config(config, data_length=data_length)

        with open(file_name, 'w') as file:
            file.write('# cmpl = %f (A); V_1 = %f (V); V_2 = %f (V);'
                       '\n' % (self.cmpl, self.v_1, self.v_2))
            file.write('# points = %d; delay = %f (s); speed = %f (s);'
                       '\n' % (self.points, self.delay, self.speed))
            file.write('# Voltage (V) |  Current (A)  |  Time (s)\n')
            for i in range(self._data_length):
                file.write('%+8.6E   %+8.6E   %+8.6E'
                           '\n' % (data[i, 0], data[i, 1], data[i, 2]))
