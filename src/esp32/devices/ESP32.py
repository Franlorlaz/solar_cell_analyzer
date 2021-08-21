"""ESP32 Main Class Definition."""

import serial
import serial.tools.list_ports
from .ESP32Simulator import ESP32Simulator


class ESP32:
    """Arduino main class."""

    def __init__(self, port=None):
        """Initialize ESP32 object connecting to a port."""
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
            self.ser = ESP32Simulator()

        self.port = port
        print('ESP32 connected to: ', port)
        return self.ser

    def disconnect(self):
        """Disconnect ESP32 and connect to ESP32Simulator.

        :return: A serial object.
        """
        self.ser.close()
        self.port = None
        self.ser = ESP32Simulator()
        print('ESP32 disconnected')
        return self.ser

    def switch_relay(self, cell=1, electrode_id=1, switch_off=False):
        """Send open/close relay order to ESP32.

        :param cell: Cell number (integer).
        :param electrode_id: Electrode number (integer).
        :param switch_off: Switch off all relays or not (boolean).
        :return: A dictionary with used parameters.
        """
        relay = 4 * int(cell) + int(electrode_id)
        self.ser.write(b'\x00')  # switch off all
        if not switch_off:
            self.ser.write(b'c' + relay.to_bytes(1, 'big'))

        return {'cell': cell, 'electrode_id': electrode_id,
                'switch_off': switch_off}

    def polarize(self, voltage, calibration=None):
        """Send polarize order to ESP32.

        :param voltage: voltage to set by ESP32. If calibration is not
        given, voltage must be an integer between 0 and 255.
        :param calibration: Dict with calibration parameters. It must have
        the keys {'a', 'b'}. Equation: y = a*x + b
        :return: A dictionary with used parameters.
        """
        a = 1
        b = 0

        if calibration:
            if 'a' not in calibration and 'b' not in calibration:
                raise ValueError('The calibration parameter given to '
                                 'polarize() is not correct. It must be '
                                 'like: {"a"=1, "b"=0}.')
            if 'a' in calibration:
                a = float(calibration['a'])
            if 'b' in calibration:
                b = float(calibration['b'])

        voltage = int(a * voltage + b)
        self.ser.write(b'd' + voltage.to_bytes(1, 'big'))

        return {'voltage': voltage, 'calibration': calibration}