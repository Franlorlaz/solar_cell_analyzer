"""Section 3: save path configuration and run button"""
# TODO: Arduino object instantiation
# TODO: config/tmp/mode.json antes de empezar
# TODO: config/tmp/param.txt como te pongo los datos ahí

import json
from subprocess import Popen
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from py.PopUps.MeasurePopup import MeasurePopup
from py.PopUps.PolarizePopup import PolarizePopup
from py.PopUps.ErrorWarning import ErrorWarningPopup


class Section3(BoxLayout):
    id_section3 = ObjectProperty(None)
    init_dir = StringProperty('')

    def __init__(self, **kwargs):
        super(Section3, self).__init__(**kwargs)
        self.init_dir = str(Path(__file__ + '/../../../../measures').resolve())
        self.keithley = None
        self.arduino = 'Arduino object: '

        self.repeat_electrode = False
        self.repeat_all = False
        self.have_to_wait = False
        self.wait = 2.0
        self.sequence = []
        self.basic_sequence = []
        self.program = []

    def make_interface_dict(self):
        section1 = self.parent.parent.ids.section1
        section2 = self.parent.parent.ids.section2
        section3 = self.parent.parent.ids.section3

        saving_directory = section3.ids.directory_label.text
        # FIXME: el string es "['/path/directory']" pero
        #  deberia ser "/path/directory". Esto da problemas.
        saving_directory = saving_directory[2:-2]
        # FIXME: solucion provisional. Quitar esta linea cuando se arregle

        mode_name = section1.ids.mode_spinner.text
        mode_config = Path(__file__ + '/../../../../config/tmp/mode.json')
        if section1.ids['polarize_check'].active:
            polarize = True
        else:
            polarize = False

        types = ['no_repetition', 'electrode_repetition', 'all_repetition']
        # FIXME: change the list to ['', 'electrode', 'all']
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
                              'config': str(mode_config.resolve())},
                              'polarize': bool(polarize),
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

    def Start_button(self):  # FIXME: change to lower case
        # Initialize param.txt as empty file
        param_path = Path(__file__ + '/../../../../config/tmp/param.txt')
        param_path = param_path.resolve()
        with open(param_path, 'w') as f:
            f.write('')

        # Initialize trigger.json as False
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        trigger['stop_button'] = False
        trigger['measuring'] = False
        with open(trigger_path, 'w') as f:
            json.dump(trigger, f, indent=2)

        # Generate de global_dict
        data = self.make_interface_dict()

        # variables
        repeat_electrode = data['repeat']['type'] == 'electrode_repetition'
        # FIXME: change to 'electrode'
        repeat_all = data['repeat']['type'] == 'all_repetition'
        # FIXME: change to 'all'

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

        # Open Measure Popup and run
        polarize = data['mode']['polarize']
        if polarize:
            measure = PolarizePopup()
            measure.open()
        else:
            measure = MeasurePopup()
            measure.open()
        measure.display_measure()

        self.sequence = sequence
        self.basic_sequence = basic_sequence
        self.repeat_electrode = repeat_electrode
        self.repeat_all = repeat_all
        self.wait = data['repeat']['wait']
        self.program = []

        for iteration in sequence:
            cell_name = data['cells']['cell_' + iteration[0]]['name']
            program = {'mode': str(data['mode']['name']),
                       'cell_name': str(cell_name),
                       'electrode': str(iteration[1]).upper(),
                       'directory': str(data['saving_directory']),
                       'config': str(data['mode']['config']),
                       'keithley': self.keithley,
                       'trigger_path': str(trigger_path),
                       'param_path': str(param_path)}
            self.program.append(program)

        Clock.schedule_once(self.run, 1)

    def run(self, *dt):
        wait = 2.0
        program_path = Path(__file__ + '/../../../../config/tmp/program.json')
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)

        if self.have_to_wait and not trigger['measuring']:
            trigger['measuring'] = True
            wait += self.wait
            self.have_to_wait = False

        if not trigger['measuring'] and not trigger['stop_button']:
            if self.sequence:
                iteration = self.sequence.pop(0)
                program = self.program.pop(0)

                print(self.arduino, iteration)  # TODO: switch on relay
                with open(program_path.resolve(), 'w') as f:
                    json.dump(program, f, indent=2)

                Popen(['python3', 'keithley/CLI.py', 'run', '--program',
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
                trigger['stop_button'] = True
                # FIXME: Change label from 'Stop' to 'Volver'
                # FIXME: The button need two clicks, fix this

        if not trigger['stop_button']:
            Clock.schedule_once(self.run, wait)
