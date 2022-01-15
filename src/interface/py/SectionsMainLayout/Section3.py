"""Section 3: save path configuration and run button"""

import json
from subprocess import Popen
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from interface.py.PopUps.MeasurePopup import MeasurePopup
from interface.py.PopUps.PolarizePopup import PolarizePopup
from interface.py.PopUps.CalibrationPopup import CalibrationPopup
from interface.py.PopUps.ConfirmCalibrationPopup import ConfirmCalibrationPopup
from interface.py.PopUps.ErrorWarningPopup import ErrorWarningPopup
from arduino import Arduino
from esp32 import ESP32, polarize
import datetime

class Section3(BoxLayout):
    """Section 3 (save path configuration and run) class."""
    id_section_3 = ObjectProperty(None)
    init_dir = StringProperty('')
    init_dir_clipped = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize attributes."""
        super(Section3, self).__init__(**kwargs)
        self.initializing_popup = Popup(title='',
                                        content=Label(text='Initializing...'),
                                        size_hint=(None, None),
                                        size=(300, 200))

        self.init_dir = str(Path(__file__ + '/../../../../measures').resolve())
        self.init_dir_clipped = '...' + self.init_dir[-33:]
        self.msg = ''
        self.keithley = None
        self.arduino = Arduino(port=None)
        self.esp32 = ESP32(port=None)

        self.repeat_electrode = False
        self.repeat_all = False
        self.have_to_wait = False
        self.wait = 2.0
        self.sequence = []
        self.basic_sequence = []
        self.program = []
        self.checkbox_polarize = False
        self.measure_popup = MeasurePopup()
        self.confirm_calibration_popup = ConfirmCalibrationPopup()

        param_path = Path(__file__ + '/../../../../config/tmp/param.json')
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        mode_path = Path(__file__ + '/../../../../config/tmp/mode.json')
        calib_path = Path(__file__+'/../../../../config/tmp/calibration.json')
        polar_path = Path(__file__+'/../../../../config/tmp/polarization.json')
        self.paths = {'param_path': param_path.resolve(),
                      'trigger_path': trigger_path.resolve(),
                      'mode_path': mode_path.resolve(),
                      'calibration_path': calib_path.resolve(),
                      'polarization_path': polar_path.resolve()}

    def check_params(self, sequence, arduino, esp32, keithley):
        """Check that:
            a) An electrode has been selected to measure
            b) A port has been selected for the arduino
            c) A port has been selected for the esp32
            d) A port has been selected for the keithley

        :param sequence: A list that contains electrode sequence to measure.
        :param arduino: An object that contains information about arduino.
        :param esp32: An object that contains information about esp32.
        :param keithley: An object that contains information about keithley.

        :return: True, if there is any error;
                 False, otherwise.
        """

        self.msg = ''
        if not sequence:
            self.msg += 'No electrode selected. \n\n'
        if arduino.port is None:
            self.msg += 'No port selected for Arduino.\n\n'
        if esp32.port is None:
            self.msg += 'No port selected for ESP32.\n\n'
        if keithley is None:
            self.msg += 'No port selected for Keithley.\n\n'

        if self.msg != '':
            return False
        else:
            return True

    def make_interface_dict(self):
        """Generate the dictionary with the interface configuration."""
        section1 = self.parent.parent.ids.section1
        section2 = self.parent.parent.ids.section2
        section3 = self.parent.parent.ids.section3

        saving_directory = section3.init_dir

        mode_name = section1.ids.mode_spinner.text
        mode_config = Path(__file__ + '/../../../../config/tmp/mode.json')
        if section1.ids['polarize_check'].active:
            polarize = True
        else:
            polarize = False

        types = ['no_repetition', 'electrode_repetition', 'all_repetition']
        repeat_type = list(filter(lambda par: section1.ids[par].active, types))
        repeat_times = section1.ids.number_repetition.text
        repeat_wait = section1.ids.time_repetition.text

        electrodes = ['a', 'b', 'c', 'd']
        cells = {'cell_1': {}, 'cell_2': {}, 'cell_3': {}, 'cell_4': {}}
        for cell, value in cells.items():
            value['name'] = str(section2.ids['textinput_' + cell].text)
            value['electrodes'] = list(filter(lambda i:
                                              section2.ids[cell + i].active,
                                              electrodes))

        interface = {'saving_directory': str(saving_directory),
                     'mode': {'name': str(mode_name).lower(),
                              'config': str(mode_config.resolve()),
                              'polarize': bool(polarize)},
                     'repeat': {'type': str(repeat_type[0]),
                                'times': int(repeat_times),
                                'wait': float(repeat_wait)},
                     'cells': cells
                     }

        interface_json = Path(__file__ +
                              '/../../../../config/tmp/interface.json')
        with open(interface_json.resolve(), 'w') as f:
            json.dump(interface, f, indent=2)

        return interface

    def start_button(self):
        """Start the measurement process."""
        # config files
        param_path = self.paths['param_path']
        trigger_path = self.paths['trigger_path']
        mode_path = self.paths['mode_path']
        calibration_path = self.paths['calibration_path']
        polarization_path = self.paths['polarization_path']

        # Initialize param.json as empty file
        param_path = param_path.resolve()
        with open(param_path, 'w') as f:
            json.dump([], f, indent=2)

        # Initialize trigger.json as False
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        trigger['stop_button'] = False
        trigger['measuring'] = False
        with open(trigger_path, 'w') as f:
            json.dump(trigger, f, indent=2)

        # Initialize Stop button in measure popup
        self.measure_popup.ids.stop_button.text = 'Stop'

        # Generate de global_dict
        data = self.make_interface_dict()

        # Change mode in mode.json
        mode_path = mode_path.resolve()
        with open(mode_path, 'r') as f:
            mode = json.load(f)
        mode['mode'] = data['mode']['name']
        with open(mode_path, 'w') as f:
            json.dump(mode, f, indent=2)

        # variables
        repeat_electrode = data['repeat']['type'] == 'electrode_repetition'
        repeat_all = data['repeat']['type'] == 'all_repetition'

        # sequence of measures
        sequence = []
        for key, value in data['cells'].items():
            number = key.split('_')[-1]
            for electrode in value['electrodes']:
                sequence.append(number + electrode)
                if repeat_electrode:
                    for _ in range(data['repeat']['times']):
                        sequence.append(number + electrode)
        basic_sequence = list(sequence)
        if repeat_all:
            sequence *= data['repeat']['times'] + 1

        # Check params
        trigger_check = \
            self.check_params(sequence, self.arduino,
                              self.esp32, self.keithley)

        self.sequence = sequence
        self.basic_sequence = basic_sequence
        self.repeat_electrode = repeat_electrode
        self.repeat_all = repeat_all
        self.wait = float(data['repeat']['wait']) * 60
        self.program = []

        for iteration in sequence:
            cell_name = data['cells']['cell_' + iteration[0]]['name']
            program = {'mode': str(data['mode']['name']),
                       'cell_name': str(cell_name),
                       'cell_id': int(iteration[0]),
                       'electrode': str(iteration[1]).upper(),
                       'directory': str(data['saving_directory']),
                       'config': str(data['mode']['config']),
                       'keithley': self.keithley,
                       'trigger_path': str(trigger_path),
                       'param_path': str(param_path),
                       'polarization_path': str(polarization_path.resolve())}
            self.program.append(program)

        # Open Polarize or Measure Popup and run
        checkbox_polarize = data['mode']['polarize']
        self.checkbox_polarize = checkbox_polarize
        if checkbox_polarize:
            measure = PolarizePopup()
            unique_sequence = list(set(sequence))
            unique_sequence.sort()
            measure.pass_arg(unique_sequence, self)
            measure.open()
        else:
            # References zero time for degradation. Deeper changes should be done here
            degrad0time_path = Path(__file__ + '/../../../../config/tmp/DegradationZeroTime.txt')
            now = datetime.datetime.now()
            with open(degrad0time_path.resolve(), 'w') as f:
                f.write(str(now))
            measure = self.measure_popup
            measure.reset_measure()
            measure.open()
            Clock.schedule_once(self.run, 1)

        if not trigger_check:
            error_warning_popup = ErrorWarningPopup()
            error_warning_popup.open()
            error_warning_popup.print_error_msg(self.msg)

        self.initializing_popup.open()
        Clock.schedule_once(self.initial_polarization, 0.1)

    def initial_polarization(self, dt):
        # Initialize polarization.json to 0.0 volts
        calibration_path = self.paths['calibration_path'].resolve()
        polarization_path = self.paths['polarization_path'].resolve()
        polarize(self.esp32, polarization_path, calibration_path,
                 reset=True)
        self.initializing_popup.dismiss()

    def run(self, *dt):
        program_path = Path(__file__ + '/../../../../config/tmp/program.json')
        param_path = Path(__file__ + '/../../../../config/tmp/param.json')
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        calibration_path = Path(__file__ +
                                '/../../../../config/tmp/calibration.json')
        polarization_path = Path(__file__ +
                                 '/../../../../config/tmp/polarization.json')

        wait = 2.0
        param_path = param_path.resolve()
        trigger_path = trigger_path.resolve()
        calibration_path = calibration_path.resolve()
        polarization_path = polarization_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)

        if self.checkbox_polarize:
            polarize(self.esp32, polarization_path, calibration_path)

        with open(param_path, 'r') as f:
            param = json.load(f)
        if len(param) > 5:
            param = param[::-1][0:5][::-1]
        self.measure_popup.display_measure(param)

        if self.have_to_wait and not trigger['measuring'] and self.sequence:
            print('---\n--- HAVE TO WAIT\n---')
            trigger['measuring'] = True
            wait += self.wait
            self.have_to_wait = False

        if not trigger['measuring'] and not trigger['stop_button']:
            if self.sequence:
                electrodes = ['A', 'B', 'C', 'D']
                iteration = self.sequence.pop(0)
                program = self.program.pop(0)
                with open(program_path.resolve(), 'w') as f:
                    json.dump(program, f, indent=2)

                cell_id = int(iteration[0])
                electrode_id = electrodes.index(iteration[1].upper()) + 1
                self.arduino.switch_relay(cell=cell_id,
                                          electrode_id=electrode_id)

                Popen(['python', 'keithley/CLI.py', 'run', '--program',
                       str(program_path.resolve())])

                repeat_all = self.repeat_all
                repeat_all_now = iteration == self.basic_sequence[-1]
                repeat_electrode = self.repeat_electrode
                if repeat_electrode or (repeat_all and repeat_all_now):
                    self.have_to_wait = True

                trigger['measuring'] = True
                with open(trigger_path, 'w') as f:
                    json.dump(trigger, f, indent=2)
            else:
                self.have_to_wait = False
                self.arduino.switch_relay(switch_off=True)
                trigger['stop_button'] = True
                self.measure_popup.ids.stop_button.text = 'Finish'
                polarize(self.esp32, polarization_path, calibration_path,
                         reset=True)

        if not trigger['stop_button']:
            Clock.schedule_once(self.run, wait)
        else:
            self.have_to_wait = False
            polarize(self.esp32, polarization_path, calibration_path,
                     reset=True)

    def press_calibrate(self):
        """Open the confirmation popup to start the calibration."""
        self.confirm_calibration_popup.open()
        self.confirm_calibration_popup.pass_arduino_1(self)

        msg = ''
        if self.arduino.port is None:
            msg += 'No port selected for Arduino.\n\n'
        if self.esp32.port is None:
            msg += 'No port selected for ESP32.\n\n'
        if self.keithley is None:
            msg += 'No port selected for Keithley.\n\n'

        if msg != '':
            error_warning_popup = ErrorWarningPopup()
            error_warning_popup.open()
            error_warning_popup.print_error_msg(msg)
