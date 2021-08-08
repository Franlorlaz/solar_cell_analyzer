"""Command Line Interface for Arduino Controller.

Usage:
$ python3 arduino/CLI.py ports
$ python3 arduino/CLI.py connect --port <str>
>> open <int><str>
>> close all
>> disconnect
"""

import cmd
import argparse

from devices.Arduino import Arduino


class ArduinoShell(cmd.Cmd):
    """Arduino Shell interface configuration."""

    intro = ("\n--- Arduino Shell ---\n"
             "Type `help` or `?` to list commands and `disconnect` to exit.\n")
    prompt = '>> '

    def __init__(self, arduino_object, **kwargs):
        """Initialize the shell with connection to the device `ser`."""
        super().__init__(**kwargs)
        self.arduino = arduino_object

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

    def do_open(self, arg):
        """Open relay.

        Type a number (cell) and a letter (electrode).
        Numbers allowed: {1, 2, 3, 4}
        Letters allowed: {A, B, C, D} and {a, b, c, d}
        Example 1: >> open 1A
        Example 2: >> open 4D
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

        self.arduino.switch_relay(cell=cell, electrode_id=electrode_id)

    def do_close(self, arg):
        """Close relay.

        Type 'all' to close all relays.
        Closing individual relays is not implemented yet.
        """
        if arg == 'all':
            self.arduino.switch_relay(switch_off=True)
        else:
            print(f'Unrecognized close option: {arg}')

    def do_disconnect(self, arg):
        """Disconnect the device and exit the interactive session."""
        self.arduino.disconnect()
        return True


if __name__ == '__main__':
    print('Arduino Relay Controller.\n')

    parser = argparse.ArgumentParser(description="Arduino Relay Controller.")

    parser.add_argument('action', type=str,
                        help='Accepted values: {ports, connect}')
    parser.add_argument('-p', '--port', type=str, help="Device for connection")
    args = parser.parse_args()

    if args.action == 'ports':
        ports = Arduino.search_ports()
        print('--- Ports ---')
        for port in ports:
            print(port)
        print('')

    elif args.action == 'connect':
        if args.port == 'None':
            args.port = None
        arduino = Arduino(port=args.port)
        ArduinoShell(arduino).cmdloop()

    else:
        print(f'Unrecognized command: {args.action}')
