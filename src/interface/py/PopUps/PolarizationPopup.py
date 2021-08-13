"""" Popup to polarization configuration"""

import json
from pathlib import Path
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class PolarizationPopup(Popup):
    id_polarizationpopup = ObjectProperty(None)

    def dict_polarization(self):
        params_polarization_lst = [
            'param_v_start',
            'param_v_stop',
            'param_points',
            'param_speed',
            'param_delay',
            'param_cmpl',
            'param_light_power',
            'param_area'
        ]

        params_polarization = dict()
        for par in params_polarization_lst:
            the_reference = self.ids[par]
            params_polarization[par] = float(the_reference.text or 0)
            the_reference.text = the_reference.text

        dict_polarization = {'mode': 'Polarization',
                       'config': params_polarization}

        # Create mode.json
        mode_path = Path(__file__ + '/../../../../measures/mode.json')
        mode_path = mode_path.resolve()
        with open(mode_path, 'w') as f:
            json.dump(dict_polarization, f, indent=2)
        print(dict_polarization)