"""Command Line Interface for ESP32 Controller.

Usage:
$ python3 esp32/CLI.py ports
$ python3 esp32/CLI.py connect --port <str>
>> channel <int><str>
>> polarize <int>
>> polarize <float> <float> <float>
>> reset_calibration
>> disconnect
"""

import cmd
import argparse
import json
from pathlib import Path

from devices.ESP32 import ESP32


class ESP32Shell(cmd.Cmd):
    """ESP32 Shell interface configuration."""

    intro = ("\n--- ESP32 Shell ---\n"
             "Type `help` or `?` to list commands and `disconnect` to exit.\n")
    prompt = '>> '

    def __init__(self, esp32_object, **kwargs):
        """Initialize the shell with connection to the device `ser`."""
        super().__init__(**kwargs)
        self.esp32 = esp32_object

    @staticmethod
    def do_exit(_arg):
        """Exit the interactive session."""
        return True

    @staticmethod
    def do_quit(_arg):
        """Exit the interactive session."""
        return True

    def emptyline(self):
        """Skip to the next line when enter an empty line."""
        pass

    def do_channel(self, arg):
        """Set the ESP32 channel.

        Example: >> channel 1A
        """
        allowed_cells = ['1', '2', '3', '4']
        allowed_electrodes = {'A': 1, 'B': 2, 'C': 3, 'D': 4,
                              'a': 1, 'b': 2, 'c': 3, 'd': 4}
        if len(arg) != 2:
            print(f'Unrecognized command "{arg}". Must be: <int><str>.'
                  ' Example: >> open 1A')
            return None

        if arg[0] in allowed_cells:
            cell = int(arg[0])
        else:
            cell = 1
            print(f'Unrecognized cell: {arg[0]}')
            print('Getting default value: cell=1')

        if arg[1] in allowed_electrodes:
            electrode_id = allowed_electrodes[arg[1]]
        else:
            electrode_id = 1
            print(f'Unrecognized electrode: {arg[1]}')
            print('Getting default value: electrode="A"')

        self.esp32.set_channel(cell=cell, electrode_id=electrode_id)

    def do_polarize(self, arg):
        """Send polarize order to ESP32.

        Can take one argument (integer voltage from 0 to 255) or
        three arguments (float voltage, a, b), where a and are parameters
        from de equation y=ax+b.

        Example 1: >> polarize 230
        Example 2: >> polarize 1.2 1.0 0.0
        """
        args = arg.split()
        if len(args) != 3 and len(args) != 1:
            print(f'Unrecognized command "{arg}". '
                  f'Must be: <float> <float> <float>.'
                  f' Example: >> polarize 1.2 1.0 0.0')
            return None
        a = 1
        b = 0
        if len(args) == 3:
            a = float(args[1])
            b = float(args[2])
        self.esp32.polarize(float(args[0]), calibration={'a': a, 'b': b})

    @staticmethod
    def do_reset_calibration(arg):
        """Reset the calibration file to default values."""
        cells = ['1', '2', '3', '4']
        elects = ['A', 'B', 'C', 'D']
        base_dir = Path(__file__ + '/../../config').resolve()
        calib_path = base_dir.joinpath(arg).resolve()
        with open(calib_path, 'r') as f:
            calibration = json.load(f)
        for cell in cells:
            for elect in elects:
                iteration = cell + elect
                calibration[iteration] = {'a': 1, 'b': 0, 'r2': 0}
        with open(calib_path.resolve(), 'w') as f:
            json.dump(calibration, f, indent=2)

    def do_disconnect(self, arg):
        """Disconnect the device and exit the interactive session."""
        self.esp32.disconnect()
        return True


if __name__ == '__main__':
    print('ESP32 Controller.\n')

    parser = argparse.ArgumentParser(description="ESP32 Controller.")

    parser.add_argument('action', type=str,
                        help='Accepted values: {ports, connect}')
    parser.add_argument('-p', '--port', type=str, help="Device for connection")
    args = parser.parse_args()

    if args.action == 'ports':
        ports = ESP32.search_ports()
        print('--- Ports ---')
        for port in ports:
            print(port)
        print('')

    elif args.action == 'connect':
        if args.port == 'None':
            args.port = None
        esp32 = ESP32(port=args.port)
        ESP32Shell(esp32).cmdloop()

    else:
        print(f'Unrecognized command: {args.action}')
