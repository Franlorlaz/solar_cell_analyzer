"""Arduino Main Class Definition."""

import serial
import serial.tools.list_ports
from .ArduinoSimulator import ArduinoSimulator


class Arduino:
    """Arduino main class."""

    def __init__(self, port=None):
        """Initialize Arduino object connecting to a port."""
        self.port = port
        self.ser = self.connect(port, disconnect_before=False)

    @staticmethod
    def search_ports():
        """List all available ports.

        This function uses 'serial.tools.list_ports' and obtain a list
        of 'ListPortInfo' object that can be iterated with the for loop
        'for port, desc, hwid in ports:'. The objects also have a 'device'
        attribute, which is returned at the end.

        :return: A list of available devices (strings).
        """
        ports = sorted(serial.tools.list_ports.comports())
        devices = [i.device for i in ports]
        return devices

    def connect(self, port, disconnect_before=True):
        """Connect to the indicated port.

        :param port: A string with the port to connect (device).
        :param disconnect_before: Disconnect or not (boolean) the current
        device before connecting to the new one.
        :return: A serial object.
        """
        if disconnect_before:
            self.disconnect()

        if port:
            self.ser = serial.Serial(port)
        else:
            self.ser = ArduinoSimulator()

        self.port = port
        print('Arduino connected to: ', port)
        return self.ser

    def disconnect(self):
        """Disconnect arduino and connect to ArduinoSimulator.

        :return: A serial object.
        """
        self.ser.close()
        self.port = None
        self.ser = ArduinoSimulator()
        print('Arduino disconnected')
        return self.ser

    def switch_relay(self, cell=1, electrode_id=1, switch_off=False,
                     calibration=None):
        """Send open/close relay order to arduino.

        :param cell: Cell number (integer).
        :param electrode_id: Electrode number (integer).
        :param switch_off: Switch off all relays or not (boolean).
        :param calibration: Switch on the calibration relay (boolean).
        :return: A dictionary with used parameters.
        """
        relay = 4 * (int(cell) - 1) + int(electrode_id)
        self.ser.write(b'\x00')  # switch off all
        if not switch_off:
            self.ser.write(relay.to_bytes(1, 'big'))
        if calibration is not None:
            if calibration:
                self.ser.write(b'\xff')
            else:
                self.ser.write(b'\xfe')

        return {'cell': cell, 'electrode_id': electrode_id,
                'switch_off': switch_off}
