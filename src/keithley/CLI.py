"""Command Line Interface for Keithley Controller.

Usage:
$ python3 keithley/CLI.py ports
$ python3 keithley/CLI.py connect --port <str>
>> config <file>
>> lineal
>> hysteresis
>> save data <file>
>> save pv_param <file> <name>
>> disconnect
"""

import cmd
import argparse
import json
from pathlib import Path

from devices.Keithley import Keithley
from utils.pv_param import calculate_pv_param, save_pv_param
from utils.path_maker import make_file


class KeithleyShell(cmd.Cmd):
    """Arduino Shell interface configuration."""

    intro = ("\n--- Keithley Shell ---\n"
             "Type `help` or `?` to list commands and `disconnect` to exit.\n")
    prompt = '>> '

    def __init__(self, keithley_object, **kwargs):
        """Initialize the shell."""
        super().__init__(**kwargs)

        self.keithley = keithley_object

        self.config = None
        self.pv_param = None

        self.dir_config = Path(__file__ + '/../../config')
        self.dir_measures = Path(__file__ + '/../../measures')
        print('Config directory: ', self.dir_config.resolve())
        print('Measures directory: ', self.dir_measures.resolve())

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
            "points": 401,
            "speed": 0.240,
            "delay": 0.001,
            "cmpl": 0.05,
            "light_power": 1.0,
            "area": 0.14,
            }
        }
        Example: >> config default/mode.json
        """
        config_json = self.dir_config.joinpath(str(arg)).resolve()
        with open(config_json, 'r') as file:
            config = json.load(file)
        self.keithley.set_config(config['config'])
        self.config = config['config']

    def do_lineal(self, arg):
        """Run the lineal mode and calcule photovoltaic parameters."""
        self.keithley.set_sensors()
        self.keithley.set_source()
        self.keithley.source_sweep_mode()
        self.keithley.set_trigger()
        self.keithley.set_display()
        data = self.keithley.run(mode='lineal')

        area = self.config['area']
        light_power = self.config['light_power']
        pv_param = calculate_pv_param(data, area=area, light_power=light_power)
        for key, value in pv_param.items():
            print(key, value, sep=': ')
        self.pv_param = [pv_param]

    def do_hysteresis(self, arg):
        """Run the hysteresis mode and calcule photovoltaic parameters."""
        self.keithley.set_sensors()
        self.keithley.set_source()
        self.keithley.source_list_mode()
        self.keithley.set_trigger()
        self.keithley.set_display()
        data = self.keithley.run(mode='hysteresis')

        points = self.keithley.points
        area = self.config['area']
        light_power = self.config['light_power']
        pv_param_1 = calculate_pv_param(data[0:points, :],
                                        area=area, light_power=light_power)
        pv_param_2 = calculate_pv_param(data[points:, :],
                                        area=area, light_power=light_power)
        for key, value in pv_param_1.items():
            print(key, (value + pv_param_2[key]) / 2, sep=': ')
        self.pv_param = [pv_param_1, pv_param_2]

    def do_save(self, arg):
        """Save data measure or photovoltaic parameters calculated.

        Usage: >> save <option> <file> <name>
        where <option> is "data" or "pv_param",
        <file> is the path to the file where to save (with file extension) and
        <name> is the sample name (used only with "save pv_param",
        <name> parameter is ignored for "save data").

        Example 1: >> save data file/for/data.txt
        Example 2: >> save pv_param file/for/param.txt sample_A
        """
        arg = arg.strip().split()

        if len(arg) < 2:
            print('Missing arguments.')
            print('Correct usage: >> save <option> <file> <name>')
            return

        elif len(arg) == 2:
            arg.append('')

        option = arg[0]
        file = self.dir_measures.joinpath(arg[1])
        name = arg[2]

        if option == 'data':
            file = make_file(str(file.resolve()), new=True, extension=None)
            self.keithley.save(file)

        elif option == 'pv_param':
            file = make_file(str(file.resolve()), header=True, extension=None)
            for pv_param in self.pv_param:
                save_pv_param(file, name, param=pv_param)

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
