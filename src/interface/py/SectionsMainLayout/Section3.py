"""Section 3: save path configuration and run button"""

import json
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from py.PopUps.MeasurePopup import MeasurePopup


class Section3(BoxLayout):
    id_section3 = ObjectProperty(None)

    def Start_button(self):
        # Initialize trigger.json as False
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()

        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        trigger['stop_button'] = False
        with open(trigger_path, 'w') as f:
            json.dump(trigger, f, indent=2, sort_keys=True)

        # Generate de global_dict
        self.make_global_dict()

        # Open Measure Popup
        midiendo = MeasurePopup()
        midiendo.open()

        Clock.schedule_once(self.run, 1) #TODO: Inicializar etiquetas a cero y que se actualicen
        midiendo.display_measure()

    def make_global_dict(self):
        mode_dict = dict()
        # params_mode_dict_lst = ['name','config']
        mode_dict['name'] = self.parent.ids.section1.ids.mode_spinner.text
        mode_dict['config'] = 'path/to/file/mode.json'

        repeat_dict = dict()
        # params_repeat_dict_lst = ['type', 'times', 'wait']
        print(list(self.parent.ids.section1.ids))
        for par in ['no_repetition', 'electrode_repetition', 'all_repetition']:
            the_reference = self.parent.ids.section1.ids[par]
            if the_reference.active:
                repeat_dict['type'] = par
        repeat_dict['times'] = self.parent.ids.section1.ids.number_repetition.text
        repeat_dict['wait'] = self.parent.ids.section1.ids.time_repetition.text

        cells_dict = dict()
        params_cells_dict_lst = ['cell_1', 'cell_2', 'cell_3', 'cell_4']
        for par in params_cells_dict_lst:
            i_cell = dict()
            the_reference = self.parent.ids.section2.ids['textinput_' + par]
            i_cell['name'] = the_reference.text
            i_cell['electrodes'] = []
            for i in ['A', 'B', 'C', 'D']:
                the_reference = self.parent.ids.section2.ids[par+i.lower()]
                if the_reference.active:
                    i_cell['electrodes'].append(i)
            cells_dict[par] = i_cell

        interface_dict = {
            'saving_directory': str(self.parent.ids.section3.ids.directory_label.text),
            'mode': mode_dict,
            'repeat': repeat_dict,
            'cells': cells_dict
        }
        print(interface_dict)

        # Create interface.json
        with open('interface/interface.json', 'w') as f:
            json.dump(interface_dict, f, indent=2)

    def run(self, *dt):
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        print('----- running: ', dt)
        if not trigger['stop_button']:
            Clock.schedule_once(self.run, 1)

