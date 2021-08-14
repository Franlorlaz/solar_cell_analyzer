"""Section 3: save path configuration and run button"""

import json
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
    init_path = StringProperty('')

    def __init__(self, **kwargs):
        super(Section3, self).__init__(**kwargs)
        self.init_path = str(Path(__file__ + '/../../../../measures').resolve())

    def Start_button(self):
        # Initialize trigger.json as False
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        init_trigger = {'stop_button': False}
        with open(trigger_path, 'w') as f:
            json.dump(init_trigger, f)

        # Generate de global_dict
        polarize_trigger = self.make_global_dict()

        if polarize_trigger:
            polarize_measure = PolarizePopup()
            polarize_measure.open()

        else:
            # Open Measure Popup
            normal_measure = MeasurePopup()
            normal_measure.open()

            self.run()
            Clock.schedule_once(self.run, 1)
            # normal_measure.display_measure()


    # TODO: Comprobar nombres de archivos de la seccion 2 (?)
    def make_global_dict(self):
        # Mode configuration
        mode_dict = dict()
        mode_dict['name'] = self.parent.parent.ids.section1.ids.mode_spinner.text
        mode_dict['config'] = 'src/measures/mode.json'
        the_reference = self.parent.parent.ids.section1.ids['polarize_check']
        if the_reference.active:
            mode_dict['polarize'] = 'yes'
            polarize_trigger = True
        else:
            mode_dict['polarize'] = 'no'
            polarize_trigger = False

        # Repeat configuration
        repeat_dict = dict()
        for par in ['no_repetition', 'electrode_repetition', 'all_repetition']:
            the_reference = self.parent.parent.ids.section1.ids[par]
            if the_reference.active:
                repeat_dict['type'] = par
        repeat_dict['times'] = int(self.parent.parent.ids.section1.ids.number_repetition.text)
        repeat_dict['wait'] = float(self.parent.parent.ids.section1.ids.time_repetition.text)

        # Cells configuration
        cells_dict = dict()
        params_cells_dict_lst = ['cell_1', 'cell_2', 'cell_3', 'cell_4']
        for par in params_cells_dict_lst:
            i_cell = dict()
            the_reference = self.parent.parent.ids.section2.ids['textinput_' + par]
            if the_reference.text == '':
                i_cell['name'] = 'default_name_' + par
            else:
                i_cell['name'] = the_reference.text
            i_cell['electrodes'] = []
            for i in ['A', 'B', 'C', 'D']:
                the_reference = self.parent.parent.ids.section2.ids[par+i.lower()]
                if the_reference.active:
                    i_cell['electrodes'].append(i)
            cells_dict[par] = i_cell

        # Global dictionary
        save_path = str(self.parent.parent.ids.section3.ids.directory_label.text)
        interface_dict = {
            'saving_directory': save_path,
            'mode': mode_dict,
            'repeat': repeat_dict,
            'cells': cells_dict
        }
        print(interface_dict)

        # Create interface.json
        interface_path = Path(__file__ + '/../../../../measures/interface.json')
        interface_path = interface_path.resolve()
        with open(interface_path, 'w') as f:
            json.dump(interface_dict, f, indent=2)

        return polarize_trigger

    def run(self, *dt):
        trigger_path = Path(__file__ + '/../../../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        print('----- running: ', dt)
        if not trigger['stop_button']:
            Clock.schedule_once(self.run, 1)

