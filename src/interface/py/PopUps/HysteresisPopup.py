"""" Popup to hysteresis configuration"""

import json
from pathlib import Path
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from ..PopUps.ErrorWarning import ErrorWarningPopup


class HysteresisPopup(Popup):
    id_hysteresis_popup = ObjectProperty(None)

    def make_hysteresis_dict(self):
        params_hysteresis_lst = [
            'param_v_start',
            'param_v_stop',
            'param_points',
            'param_speed',
            'param_delay',
            'param_cmpl',
            'param_light_power',
            'param_area'
        ]

        params_hysteresis = dict()
        trigger = True
        for par in params_hysteresis_lst:
            the_reference = self.ids[par]
            params_hysteresis[par] = float(the_reference.text or 0)
            the_reference.text = the_reference.text
            if the_reference.text == '':
                error_warning_popup = ErrorWarningPopup()
                error_warning_popup.open()
                msg = 'Some of the configuration parameters have not been filled in.'
                error_warning_popup.print_error_msg(msg)
                trigger = False
                break
            if float(the_reference.text) < 0.0:
                error_warning_popup = ErrorWarningPopup()
                error_warning_popup.open()
                msg = 'Some of the configuration parameters have a negative value. All parameters have to be positive or null.'
                error_warning_popup.print_error_msg(msg)
                trigger = False
                break

        while trigger:
            dict_hysteresis = {'mode': 'Hysteresis',
                               'config': params_hysteresis}

            # Create mode.json
            mode_path = Path(__file__ + '/../../../../measures/mode.json')
            mode_path = mode_path.resolve()
            with open(mode_path, 'w') as f:
                json.dump(dict_hysteresis, f, indent=2)
            print(dict_hysteresis)

            trigger = False
            self.dismiss()