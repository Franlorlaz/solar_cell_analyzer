"""" Popup to lineal configuration"""

import json
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class LinealPopup(Popup):
    id_linealpopup = ObjectProperty(None)

    def dict_lineal(self):
        params_lineal_lst = [
            'param_v_start',
            'param_v_stop',
            'param_points',
            'param_speed',
            'param_delay',
            'param_cmpl',
            'param_light_power',
            'param_area'
        ]

        params_lineal = dict()
        for par in params_lineal_lst:
            the_reference = self.ids[par]
            params_lineal[par] = float(the_reference.text or 0)
            the_reference.text = the_reference.text

        dict_lineal = {'mode': 'Lineal',
                       'config': params_lineal}

        # Create mode.json
        with open('interface/mode.json', 'w') as f:
            json.dump(dict_lineal, f, indent=2)
        print(dict_lineal)