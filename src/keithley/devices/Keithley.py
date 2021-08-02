
# TODO: keithley
# TODO: keithley save

import numpy as np
import pyvisa as visa
from .KeithleySimulator import KeithleySimulator


class Keithley:

    def __init__(self, port=None, mode='sweep', v_1=1.2, v_2=-0.1, points=200,
                 speed=0.240, delay=0.001, cmpl=0.05, **kwargs):
        """Initialize."""
        self.port = port
        self.inst = self.open_resource(port=port)

        self.mode = mode
        self.v_1 = v_1
        self.v_2 = v_2
        self.points = points
        self.speed = speed
        self.delay = delay
        self.cmpl = cmpl

        self._data_length = points

    @staticmethod
    def search_ports():
        resources = visa.ResourceManager().list_resources()
        return resources

    def open_resource(self, port='GPIB0::24::INSTR'):
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

    def set_config(self, config):
        self.mode = config['mode']
        self.v_1 = config['v_1']
        self.v_2 = config['v_2']
        self.points = config['points']
        self.speed = config['speed']
        self.delay = config['delay']
        self.cmpl = config['cmpl']

    def measure(self, config=None):
        inst = self.inst
        if config:
            self.set_config(config)
        mode = self.mode
        v_1 = self.v_1
        v_2 = self.v_2
        points = self.points
        speed = self.speed
        delay = self.delay
        cmpl = self.cmpl

        if not self.port:
            return inst.measure_simulation()

        #######################################################################
        # SET SENSORS
        #######################################################################

        inst.write(':SENS:FUNC "CURR","VOLT"')   # Enable sense functions
        inst.write(':SENS:RES:MODE MAN')         # Manual resistance mode
        inst.write(':SENS:CURR:PROT %f' % cmpl)  # set the current compliance
        inst.write(':SENS:CURR:RANG 1E-3')       # current range
        inst.write(':SENS:CURR:RANG:AUTO ON')    # disable current auto range
        # inst.write(':SENS:VOLT:RANG 1')          # voltage range (measure)
        # inst.write(':SENS:VOLT:RANG:AUTO OFF')   # disable voltage auto range
        inst.write(':SENS:CURR:NPLC 1')  # curr measure speed (PowerLineCycles)
        inst.write(':SENS:VOLT:NPLC 1')  # volt measure speed (PowerLineCycles)

        #######################################################################
        # SET SOURCE
        #######################################################################

        inst.write(':SOUR:FUNC VOLT')       # volts source function
        inst.write(':SOUR:VOLT:PROT 20')    # V-source protection
        inst.write(':SOUR:DEL %f' % delay)  # source-delay-measure MANUAL
        # inst.write(':SOUR:DEL:AUTO ON')     # source-delay-measure AUTO

        if mode == 'sweep':
            self._sweep_mode(v_1, v_2, points)

        elif mode == 'list':
            points = 2 * points - 1
            voltage = Keithley._list_voltage_hysteresis(v_1, v_2, points)
            self._list_mode(voltage, points)

        self._data_length = points

        inst.write(':SOUR:VOLT:RANG 1')        # voltage range (source)
        inst.write(':SOUR:VOLT:RANG:AUTO ON')  # disable voltage auto range
        inst.write(':TRIG:COUN %f' % points)   # Trigger count
        inst.write(':TRIG:DEL %f' % speed)     # Trigger delay

        #######################################################################
        # DISPLAY
        #######################################################################

        inst.write(':DISP:WIND:TEXT:STAT OFF')            # display state
        inst.write(':DISP:WIND:TEXT:DATA "hello world"')  # display message
        inst.write(':DISP:CND')  # Return to source-measure display state

        #######################################################################
        # INITIATE, READ DATA AND FINISH
        #######################################################################

        # inst.write(':TRAC:TST:FORM DELT')  # timestamp format: ABSolute/DELTa
        inst.write(':FORM:ELEM VOLT,CURR,TIME')  # query elements in data
        inst.write(':OUTP ON')  # open output
        data = inst.query_ascii_values(':READ?', container=np.array)
        # inst.query(':TRAC:TST:FORM?')  # read timestamp format
        # inst.query(':SYST:TIME?')      # returns the current timestamp value
        inst.write(':OUTP OFF')  # close output

        return np.reshape(data, (points, 3))

    def _sweep_mode(self, v_1, v_2, points):
        """Lineal."""

        inst = self.inst
        inst.write(':SOUR:SWE:SPAC LIN')          # Linear sweep
        inst.write(':SOUR:VOLT:STAR %f' % v_1)    # start voltage
        inst.write(':SOUR:VOLT:STOP %f' % v_2)    # stop voltage
        inst.write(':SOUR:SWE:POIN %f' % points)  # Sweep points

        return {'v_1': v_1, 'v_2': v_2, 'points': points}

    def _list_mode(self, voltage, points):
        """Hysteresis."""

        inst = self.inst
        inst.write(':SOUR:VOLT:MODE LIST')           # Volts list mode
        inst.write(':SOUR:LIST:VOLT %s' % voltage)   # Volts list
        # inst.write(':SOUR:LIST:POIN %f' % points)  # Sweep points
        return {'voltage': voltage, 'points': points}

    @staticmethod
    def _list_voltage_hysteresis(v_1, v_2, points):
        step = (v_2 - v_1) / (points - 1)
        voltage = str(v_1)
        for j in range(1, points):
            voltage += ',' + str(v_1 + j * step)
        for j in range(1, points):
            voltage += ',' + str(v_1 + (points - 1 - j) * step)
        return voltage

    def save(self, data, file_name):

        with open(file_name, 'w') as file:
            file.write('# cmpl = %f (A); V_1 = %f (V); V_2 = %f (V);'
                       '\n' % (self.cmpl, self.v_1, self.v_2))
            file.write('# points = %d; delay = %f (s); speed = %f (s);'
                       '\n' % (self.points, self.delay, self.speed))
            file.write('# Voltage (V) |  Current (A)  |  Time (s)\n')
            for i in range(self._data_length):
                file.write('%+8.6E   %+8.6E   %+8.6E'
                           '\n' % (data[i, 0], data[i, 1], data[i, 2]))
