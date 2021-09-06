"""ESP32 Main Class Definition."""

import time
import serial
import serial.tools.list_ports
from .ESP32Simulator import ESP32Simulator


class ESP32:
    """Arduino main class."""

    def __init__(self, port=None):
        """Initialize ESP32 object connecting to a port."""
        self.port = port
        self.ser = self.connect(port, disconnect_before=False)
        self.wait = 0.2

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

    def set_channel(self, cell=1, electrode_id=1):
        """Set output channel to ESP32.

        :param cell: Cell number (integer).
        :param electrode_id: Electrode number (integer).
        :return: A dictionary with used parameters.
        """
        wait = 0.2
        channel = 4 * (int(cell) - 1) + int(electrode_id)
        order = 'c' + str(channel) + '\n'
        self.ser.write(order.encode())
        time.sleep(wait)

        return {'cell': cell, 'electrode_id': electrode_id}

    def polarize(self, voltage, calibration=None):
        """Send polarize order to ESP32.

        :param voltage: voltage to set by ESP32. If calibration is not
        given, voltage must be an integer between 0 and 255.
        :param calibration: Dict with calibration parameters. It must have
        the keys {'a', 'b'}. Equation: y = a*x + b
        :return: A dictionary with used parameters.
        """
        wait = self.wait
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
        order = 'd' + str(voltage) + '\n'
        self.ser.write(order.encode())
        time.sleep(wait)

        return {'voltage': voltage, 'calibration': calibration}
