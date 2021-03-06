"""" Popup to hysteresis configuration."""

import json
from pathlib import Path
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from ..PopUps.ErrorWarningPopup import ErrorWarningPopup


class HysteresisPopup(Popup):
    """Hysteresis popup class."""
    id_hysteresis_popup = ObjectProperty(None)
    param_v_1_init = NumericProperty(0.0)
    param_v_2_init = NumericProperty(0.0)
    param_points_init = NumericProperty(0)
    param_speed_init = NumericProperty(0.0)
    param_delay_init = NumericProperty(0.0)
    param_cmpl_init = NumericProperty(0.0)
    param_light_power_init = NumericProperty(0.0)
    param_area_init = NumericProperty(0.0)

    def __init__(self, **kwargs):
        """Initialize the parameters with the values from the last run."""
        super(HysteresisPopup, self).__init__(**kwargs)
        self.params_hysteresis_lst = [
            'v_1',
            'v_2',
            'points',
            'speed',
            'delay',
            'cmpl',
            'light_power',
            'area'
        ]

        path = str(Path(__file__ + '/../../../../config/tmp/mode.json').resolve())
        with open(path, 'r') as f:
            init_dict = json.load(f)

        self.param_v_1_init = init_dict['config']['v_1']
        self.param_v_2_init = init_dict['config']['v_2']
        self.param_points_init = int(init_dict['config']['points'])
        self.param_speed_init = init_dict['config']['speed']
        self.param_delay_init = init_dict['config']['delay']
        self.param_cmpl_init = init_dict['config']['cmpl']
        self.param_light_power_init = init_dict['config']['light_power']
        self.param_area_init = init_dict['config']['area']

    def make_hysteresis_dict(self):
        """Generate the dictionary with the hysteresis configuration."""
        params_hysteresis = dict()
        trigger = True

        for par in self.params_hysteresis_lst:
            the_reference = self.ids['param_' + par]
            params_hysteresis[par] = float(the_reference.text or 0)
            if par == 'points':
                params_hysteresis[par] = int(params_hysteresis[par])
            the_reference.text = the_reference.text

            if the_reference.text == '':
                error_warning_popup = ErrorWarningPopup()
                error_warning_popup.open()
                msg = 'Some of the configuration parameters have not been filled in.'
                error_warning_popup.print_error_msg(msg)
                trigger = False
                break

            if float(the_reference.text) < 0.0 and par in self.params_hysteresis_lst[2:]:
                error_warning_popup = ErrorWarningPopup()
                error_warning_popup.open()
                msg = "The configuration parameter '" + str(par) + "' has a negative value. "\
                      "It has to be positive or null."
                error_warning_popup.print_error_msg(msg)
                trigger = False
                break

        while trigger:
            dict_hysteresis = {'mode': 'hysteresis',
                               'config': params_hysteresis}

            # Create mode.json
            mode_path = Path(__file__ + '/../../../../config/tmp/mode.json')
            mode_path = mode_path.resolve()
            with open(mode_path, 'w') as f:
                json.dump(dict_hysteresis, f, indent=2)
            print(dict_hysteresis)

            trigger = False
            self.dismiss()

    def close(self):
        """Save changes to parameters in the popup
        without generating the dictionary."""
        for par in self.params_hysteresis_lst:
            the_reference = self.ids['param_' + par]
            the_reference.text = the_reference.text
        self.dismiss()
