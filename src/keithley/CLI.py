"""Command Line Interface for Keithley Controller.

Usage:
$ python3 keithley/CLI.py ports
$ python3 keithley/CLI.py connect --port <str>
>> config <file>
>> lineal
>> hysteresis
>> save data <file>
>> save pv_param <file>
>> disconnect
"""

import cmd
import argparse
import json
from pathlib import Path

from devices.Keithley import Keithley


class KeithleyShell(cmd.Cmd):
    """Arduino Shell interface configuration."""

    intro = ("\n--- Keithley Shell ---\n"
             "Type `help` or `?` to list commands and `disconnect` to exit.\n")
    prompt = '>> '

    def __init__(self, keithley_object, **kwargs):
        """Initialize the shell with connection to the device."""
        super().__init__(**kwargs)
        self.keithley = keithley_object

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

    def do_config(self, arg):
        """Configure the keithley.

        Extract the configuration dictionary from the .json file.
        The .json must contain a structure like this:
        {"mode": "Lineal",
        "config": {
            "v_1": 1.2,
            "v_2": -0.1,
            "points": 200,
            "speed": 0.240,
            "delay": 0.001,
            "cmpl": 0.05,
            "light_power": 1.0,
            "area": 0.14,
            }
        }
        Example: >> config my_folder/mode.json
        """
        config_json = Path(str(arg))  # TODO: set a root directory.
        with open(config_json, 'r') as file:
            config = json.load(file)
        self.keithley.set_config(config['config'])

    def do_lineal(self, arg):
        """Run the lineal mode and calcule photovoltaic parameters."""
        self.keithley.set_sensors()
        self.keithley.set_source()
        self.keithley.source_sweep_mode()
        self.keithley.set_trigger()
        self.keithley.set_display()
        data = self.keithley.run()
        # TODO: calcule pv_param.
        # TODO: print pv_param.
        # TODO: save pv_param in an internal property.

    def do_hysteresis(self, arg):
        """Run the hysteresis mode and calcule photovoltaic parameters."""
        self.keithley.set_sensors()
        self.keithley.set_source()
        self.keithley.source_list_mode()
        self.keithley.set_trigger()
        self.keithley.set_display()
        data = self.keithley.run()
        # TODO: calcule pv_param.
        # TODO: print pv_param.
        # TODO: save pv_param in an internal property.

    def do_save(self, arg):
        """Save data measure or photovoltaic parameters calculated.

        Example 1: >> save data file/for/data.txt
        Example 2: >> save pv_param file/for/param.txt
        """
        # TODO: set a root directory.
        option = arg[0]  # TODO: check if this is correct.
        file = arg[1]
        if option == 'data':
            self.keithley.save(file)  # TODO: check if file exist.
        elif option == 'pv_param':
            pass  # TODO: implement this.
        else:
            print(f'Unrecognized save option: {arg}')

    def do_disconnect(self, arg):
        """Disconnect the device and exit the interactive session."""
        self.keithley.close_resource()
        return True


if __name__ == '__main__':
    print('Keithley Controller.\n')

    parser = argparse.ArgumentParser(description="Keithley Controller.")

    parser.add_argument('action', type=str,
                        help='Accepted values: {ports, connect}')
    parser.add_argument('-p', '--port', type=str, help="Device for connection")
    args = parser.parse_args()

    if args.action == 'ports':
        ports = Keithley.search_ports()
        print('--- Ports ---')
        for port in ports:
            print(port)
        print('')

    elif args.action == 'connect':
        if args.port == 'None':
            args.port = None
        keithley = Keithley(port=args.port)
        KeithleyShell(keithley).cmdloop()

    else:
        print(f'Unrecognized command: {args.action}')
