"""" Popup to hysteresis configuration"""

import json
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class HysteresisPopup(Popup):
    id_hysteresispopup = ObjectProperty(None)

    def dict_hysteresis(self):
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
        for par in params_hysteresis_lst:
            the_reference = self.ids[par]
            params_hysteresis[par] = float(the_reference.text or 0)
            the_reference.text = the_reference.text

        dict_hysteresis = {'mode': 'Hysteresis',
                       'config': params_hysteresis}

        # Create mode.json
        with open('interface/mode.json', 'w') as f:
            json.dump(dict_hysteresis, f, indent=2)
        print(dict_hysteresis)